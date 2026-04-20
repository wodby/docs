# Application Backups

## Overview

If an application's stack has services that provide [backup functionality](../services/backups.md), you can run backups for the corresponding app service. The backup process consists of three steps:

- creating the backup archive in the container's ephemeral storage
- mirroring the backup to third-party object storage, such as S3 or another supported provider
- cleaning up the backup from the container's ephemeral storage

## Backup destination

When configuring a backup or backup preset, select the destination bucket only. You no longer need to select a region separately.

If the provider supports object storage classes, the storage class override is optional. If you set it, Wodby will use it for uploaded backup objects. If you leave it empty, the bucket's default storage class will be used.

## Backup presets

Backup presets are a way to save time when entering backup destination details. You can create an organization-wide preset and apply it to backup schedules.
