# Kinship Graph Schema

## Data Format: JSON (consumed by Gephi, D3.js, or Cytoscape)

```json
{
  "nodes": [
    {
      "id": "joane-greene",
      "name": "Joane Greene",
      "year_birth": "~1650",
      "year_death": "?",
      "gender": "F",
      "status": "HERO",
      "joane_link_strength": "direct",
      "sources": ["1682 deed"]
    },
    {
      "id": "john-greene-capt",
      "name": "John Greene (Capt)",
      "year_birth": "~1639",
      "gender": "M",
      "status": "PROBABLE",
      "joane_link_strength": "spouse",
      "sources": ["1679 affidavit", "1682 deed"]
    }
  ],
  "edges": [
    {
      "source": "john-greene-capt",
      "target": "joane-greene",
      "relationship": "spouse",
      "confidence": "PROBABLE",
      "evidence": "1682 deed witnesses",
      "contamination_risk": "None"
    }
  ]
}
