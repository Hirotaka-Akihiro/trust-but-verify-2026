"""Load ISCXVPN2016 Scenario B (15 s), clean, sample and split.

Outputs:
  data/processed/flows.csv      flow_id, split, label, vpn, 23 features
  results/data_manifest.json    source hash, cleaning counts, class counts per split
Run: python src/data_prep.py
"""
import hashlib
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
ZIP = ROOT / "data" / "raw" / "Scenario B-ARFF.zip"
MEMBER = "Scenario B-ARFF/TimeBasedFeatures-Dataset-15s.arff"
SEED, MAX_FLOWS = 42, 10_000
LABELS = {"BROWSING": "browsing", "CHAT": "chat", "STREAMING": "streaming", "MAIL": "email",
          "VOIP": "voip", "P2P": "p2p", "FT": "file_transfer"}


def load_arff(raw: str) -> pd.DataFrame:
    """Lenient ARFF reader: the release has stray trailing commas on every line."""
    cols, rows, in_data = [], [], False
    for line in raw.splitlines():
        line = line.strip().rstrip(",")
        if not line or line.startswith("%"):
            continue
        low = line.lower()
        if low.startswith("@attribute"):
            cols.append(line.split()[1])
        elif low == "@data":
            in_data = True
        elif in_data:
            rows.append(line.split(","))
    df = pd.DataFrame(rows, columns=cols)
    feats = cols[:-1]
    df[feats] = df[feats].apply(pd.to_numeric, errors="coerce")
    return df.rename(columns={cols[-1]: "raw_label"})


def main():
    zbytes = ZIP.read_bytes()
    with zipfile.ZipFile(ZIP) as z:
        raw = z.read(MEMBER)
    df = load_arff(raw.decode("latin-1"))
    feats = [c for c in df.columns if c != "raw_label"]
    log = {"source_zip": ZIP.name, "zip_sha256": hashlib.sha256(zbytes).hexdigest(),
           "member": MEMBER, "member_sha256": hashlib.sha256(raw).hexdigest(),
           "rows_loaded": len(df), "n_features": len(feats), "features": feats}

    df["vpn"] = df["raw_label"].str.startswith("VPN-")
    df["label"] = df["raw_label"].str.replace("VPN-", "", regex=False).map(LABELS)
    assert df["label"].notna().all(), "unmapped label"

    df[feats] = df[feats].replace([np.inf, -np.inf], np.nan)
    log["rows_with_nan_or_inf"] = int(df[feats].isna().any(axis=1).sum())
    log["rows_with_minus1_sentinel"] = int((df[feats] == -1).any(axis=1).sum())

    # Duplicates: same features. Conflicting labels -> drop all copies; same label -> keep one.
    n_labels = df.groupby(feats, dropna=False)["label"].transform("nunique")
    log["rows_in_conflicting_label_groups"] = int((n_labels > 1).sum())
    df = df[n_labels == 1]
    before = len(df)
    df = df.drop_duplicates(subset=feats + ["label"])
    log["same_label_duplicates_removed"] = before - len(df)
    log["rows_after_cleaning"] = len(df)
    log["class_counts_after_cleaning"] = df["label"].value_counts().to_dict()

    # Stratified sample to the Phase 2 workload limit, then 60/20/20 stratified split.
    if len(df) > MAX_FLOWS:
        df, _ = train_test_split(df, train_size=MAX_FLOWS, stratify=df["label"], random_state=SEED)
    train, rest = train_test_split(df, test_size=0.4, stratify=df["label"], random_state=SEED)
    val, test = train_test_split(rest, test_size=0.5, stratify=rest["label"], random_state=SEED)
    out = pd.concat([train.assign(split="train"), val.assign(split="val"), test.assign(split="test")])
    out = out.reset_index(drop=True)
    out.insert(0, "flow_id", [f"F{i:05d}" for i in range(len(out))])
    out = out[["flow_id", "split", "label", "vpn"] + feats]

    (ROOT / "data" / "processed").mkdir(parents=True, exist_ok=True)
    out.to_csv(ROOT / "data" / "processed" / "flows.csv", index=False)
    log["split_counts"] = {s: out[out.split == s]["label"].value_counts().to_dict()
                           for s in ("train", "val", "test")}
    log["split_sizes"] = out["split"].value_counts().to_dict()
    (ROOT / "results" / "data_manifest.json").write_text(json.dumps(log, indent=2))
    for k in ("rows_loaded", "rows_with_nan_or_inf", "rows_with_minus1_sentinel",
              "rows_in_conflicting_label_groups", "same_label_duplicates_removed",
              "rows_after_cleaning", "split_sizes"):
        print(f"{k}: {log[k]}")
    print("test counts:", log["split_counts"]["test"])


if __name__ == "__main__":
    main()
