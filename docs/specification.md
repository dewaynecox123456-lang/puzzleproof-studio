# PuzzleProof Studio
## Version 0.1.0-EarlyAccess

### Product Owner
BayouFinds

### Business Partner
Wonder Piece Studio

### Purpose

PuzzleProof Studio is a desktop application designed to help artists, photographers, and puzzle creators manage artwork approvals, copyright protection, image preparation, manufacturing assets, cataloging, printing, and reprints.

The application focuses on moving artwork from approved source material into puzzle-ready production assets while maintaining a complete audit trail.

The software must remain focused on puzzle production workflows and avoid unrelated features.

# Supported Platforms

## Development Platform

Fedora 42 Linux

## Production Platforms

Windows 7
Windows 8.1
Windows 10
Windows 11

# Licensing

The application shall use the standard BayouFinds offline licensing model.

Requirements:

- license.json
- Local validation only
- No online activation
- Yearly expiration support
- Seller-side license ledger
- Windows and Linux compatible
- Graceful expiration warnings

License information displayed in:

- Splash Screen
- About Screen
- Support Screen

# Product Mission

The software exists to:

1. Protect artists.
2. Protect Sean and Wonder Piece Studio.
3. Preserve copyright information.
4. Prepare manufacturing assets.
5. Catalog completed projects.
6. Support future reprints.
7. Maintain production records.

# Manufacturing Specifications

## Puzzle Print

Width: 8.83 inches
Height: 11.77 inches

## Box Sticker / Label

Width: 4.37 inches
Height: 5.10 inches

## Box Insert

Width: 3.75 inches
Height: 5.00 inches

Default DPI: 300

# Artist Workflow

Fields:

- Artist Name
- Artwork Title
- Contact Information
- Copyright Owner
- Company Name
- Project Notes
- Approval Status
- Catalog Number
- Project Origin

Project Origin:

- Artist Submission
- Company Project
- BayouFinds Original
- Wonder Piece Studio Original

# Artist Approval System

Generate:

- Artist Release Form
- Copyright Authorization
- Reproduction Permission

Approval States:

- Draft
- Pending
- Approved
- Revoked

Projects cannot be marked Manufacturing Ready unless approval exists.

# Image Processing

Supported Formats:

- PNG
- JPG
- JPEG
- DOCX

Functions:

- Import Artwork
- Apply preset crop
- Apply preset resize
- Export

Export Targets:

- Puzzle Print
- Box Insert
- Box Sticker / Label

DOCX export exists as transition compatibility for users who currently rely on Microsoft Word as a manual workaround. Word is not a core technical requirement. PNG and JPG exports remain available for direct print-ready image workflows. The workflow must stay focused on preset-based output generation from one customer image and these three production outputs; batch processing and social media package generation are not part of this release scope.

# Copyright System

Profiles:

1. Wonder Piece Studio
2. BayouFinds
3. Artist Copyright
4. Company Copyright
5. Custom

Options:

- Placement
- Opacity
- Font Size
- Color

Locations:

- Bottom Right
- Bottom Left
- Bottom Center

# Catalog System

Catalog ID Example:

WPS-2026-000001

Store:

- Artist
- Artwork
- Copyright
- Export History
- Print History
- Approval Status
- Manufacturing Status

Functions:

- Search
- View
- Reprint
- Re-export

# Reprint System

Users can:

- Open Previous Project
- Regenerate Exports
- Regenerate Print Assets

# Printing System

Supported Outputs:

- Artist Release
- Copyright Form
- Production Sheet
- Sticker
- Insert
- Puzzle Cover

Features:

- Print Preview
- Save PDF
- Printer Selection
- Printer Profiles

Batch Operation:

Print Production Package

# Manufacturing Ready

Requirements:

- Artist Approval Exists
- Source Image Exists
- Copyright Assigned
- Exports Generated

# BayouFinds Sample Artwork

Name:

Bayou Sunset

Description:

Louisiana bayou scene with sunset, cypress trees, reflections, and BayouFinds branding.

Purpose:

- Demonstration
- Testing
- Marketing
- Sample Puzzle

# Splash Screen

Display:

- PuzzleProof Studio
- Artist-to-Puzzle Production Utility
- Version Number
- License Status
- Wonder Piece Studio
- BayouFinds
- Copyright Notice

Duration:

2 to 3 seconds

# About Screen

Display:

- Product Name
- Version
- Copyright
- License Type
- Website
- Support Contact
- Developer Information

# Support Screen

Display:

- License Status
- License Expiration
- Support Email
- Website
- Version
- Operating System

Functions:

- Open Logs Folder
- Open Project Folder
- Copy Support Information

# Contact Information

Website:
https://bayoufinds.com

Support Email:
support@bayoufinds.com

Business:
BayouFinds / Wonder Piece Studio

# Data Storage

Projects:
jobs/

Catalog:
catalog/

Logs:
data/logs/

Settings:
data/settings/

Backups:
data/backups/

Exports:
exports/

# Feature Governance

Every new feature must satisfy at least one:

- Protect the artist
- Protect Sean
- Improve production
- Improve cataloging
- Improve printing
- Improve reprints
- Improve manufacturing

Features failing these requirements should not be added.

# Version 0.1.0 Scope

Included:

- Project Creation
- Artist Approval Tracking
- Copyright Profiles
- Image Conversion
- Manufacturing Presets
- Catalog System
- Reprint System
- Printing
- Splash Screen
- About Screen
- Support Screen
- Offline Licensing

Excluded:

- Social Media Management
- Accounting
- CRM Features
- AI Features
- Non-Puzzle Workflows
- General Image Editing Beyond Production Needs
