# Service backups

## Overview

Services can define data-backup behavior. There are two main backup methods.

### 1. Simple files backup

Wodby creates a tar archive from the specified directory. The archive can optionally be gzipped.

The resulting archive is uploaded to the object-storage bucket configured through a connected storage integration.

### 2. Through action

Wodby runs a Kubernetes job with the configured command or args override to create the backup archive. That job is expected to place the archive in the specified volume path, after which Wodby uploads it to the configured object-storage bucket.

## Template

Service backups are defined under the [`backups` section](template.md#backups) in a service template.
