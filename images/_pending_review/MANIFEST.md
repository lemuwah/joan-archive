# Image Provenance Manifest — `images/_pending_review/`

> Archivist-stage provenance for images staged for human review. Per the
> findings pipeline, no image here is public evidence until a human reviews and
> promotes it. SHA-256 anchors are recorded so any later alteration is
> detectable.

## Primary source (canonical)

### `1682_homeplace_james_instrument_manuscript_folios259-260_RIStateArchives.jpg`
- **What:** The original 17th-century manuscript page of the 24 March 1681/2
  home-place deed (John Greene [& Joan Greene his wife] → James Greene),
  folios 259–260 (a single 2-folio opening).
- **Repository:** Rhode Island State Archives — Digital Archive (Preservica).
- **Collection:** Land and Public Notary records: Volume 1, 1648–1696
  (a.k.a. RI Land Evidences Vol. I / RILE-I — the volume Worthington
  abstracted in 1921).
- **Volume folder (Preservica SO):** `SO_55976674-e8f4-44ab-b872-592c9ce4002e`
- **File (Preservica IO):** `IO_6f6b6c51-8275-4e3a-95d9-c1e205f459f7`
  (listing image `_133`).
- **Folio/image anchor:** folios 259–260; image `_133` of the volume's
  folio sequence (image↔folio navigation offset: folio = 2 × image − 7).
- **Source URL (download, no login):**
  https://sosri.access.preservica.com/download/file/IO_6f6b6c51-8275-4e3a-95d9-c1e205f459f7
- **Capture:** 600-DPI scan, 10243 × 7320 px, JPEG.
- **SHA-256:** `49cae1a721558a93b6f23f42f43562590570182e8d3c85018974d887813d5470`
- **Accessed:** 2026-09-09.
- **Caliber note:** This is the original hand — PROOF-caliber *location*; the
  *transcription* remains 🟡 AI-read pending human paleography (Law 7).

## Reading aids (derivatives — not primary sources)

Grayscale/contrast-enhanced crops of the primary scan, produced to assist
paleography of the secretary hand. Derivatives of the canonical image above;
do not cite as independent sources.

| File | Crop region | Dims | SHA-256 |
|---|---|---|---|
| `folio259_enh.jpg` | Left page (folio 259) | 5326×7320 | `929f905b1045971c8e602209ebc73a6c3a0f038a90f362e9bd38c47546e566ac` |
| `folio260_enh.jpg` | Right page (folio 260) | 5326×7320 | `353d5b870df98da7cd5c8746a774c78867a782b2d81bf90185afd674fc90f9b8` |
| `signatures_block_enh.jpg` | Witness/signature block (lower folio 260) | 5122×3294 | `5be3c360782138a12799413f06b4dfb22c85c01c6f504353747c46510f063814` |
| `..._view.jpg` variants | Downscaled (~3400 px) views of the above | varies | recorded in finding-run manifest |

## Companion source texts (re-fetchable, not staged as images)
- **Worth 1921 abstract** of this same deed (printed pp. 173–174, abstract
  [260]): Internet Archive item `rhodeislandlande00wort`;
  OCR text at `worth_djvu.txt` in repo root.
- **Typed folio index** (`Volume 1 Index`, 22 pp, lists every deed in the
  volume by grantor/grantee + folio): Preservica
  `IO_5628068c-c8fa-486c-bdb8-4ed969f46f61`; text extraction at
  `images/_preservica/vol1_index.txt`.
- **Modern name index** (27 pp, personal-name index to Worth's printed
  abstracts): Preservica `IO_2416b89e-6f8d-4510-b585-c762f4f1b338`.
- **Complete Volume PDF** (222 pp, full assembled manuscript): Preservica
  `IO_3d98349c-ffb5-4207-8c0f-66ae92bc2bc0` (1.0 GB; gitignored, re-fetchable).
