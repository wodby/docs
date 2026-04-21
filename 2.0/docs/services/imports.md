# Service imports

## Overview

Services can define data-import behavior. There are two main import methods.

### 1. Simple files import

Wodby imports files directly into the running volume by unpacking the provided tar archive to the specified path.

This method is not transactional.

### 2. Through init volume

Wodby mounts the import archive into the init volume provided by the service, and a container performs the import during startup. This pattern is commonly used for databases.

This method is transactional. Wodby starts a copy of the app service with a new persistent volume. If the import succeeds, Wodby redeploys the service using the new volume that contains the imported data.

## Template

Service imports are defined under the [`imports` section](template.md#imports) in a service template.
