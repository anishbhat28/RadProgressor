# Sample Data

This directory contains sample chest X-ray images for testing.

## Adding Sample Images

Place sample chest X-ray images here for testing the application.

Supported formats:
- DICOM (.dcm)
- PNG (.png)
- JPEG (.jpg, .jpeg)

## Demo Data

The application includes synthetic demo data that can be seeded using:

```bash
python scripts/seed_demo.py
```

This creates a demo patient (DEMO001) with 3 studies showing progression over time.
