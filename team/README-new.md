# Team Management

## Roles

Wodby provides a set of roles with the following permissions:

* **O**wners can do anything
* **A**dministrators can do anything inside of the organization
* **T**eam leaders are like administrator but can't manage servers and global team
* **D**evelopers can work with existing applications
* **U**nprivileged can't do nothing  

| Action                             | O | A | T | D | U |
| ---------------------------------- | - | - | - | - | - |
| View applications instances	     | ✓ | ✓ | ✓ | ✓ |   |
| View servers	                     | ✓ | ✓ | ✓ | ✓ |   |
| View repositories                  | ✓ | ✓ | ✓ | ✓ |   |
| View bundles                       | ✓ | ✓ | ✓ | ✓ |   |
| View integrations                  | ✓ | ✓ | ✓ | ✓ |   |
| View team     	                 | ✓ | ✓ | ✓ | ✓ |   |
| Deploy new applications            | ✓ | ✓ | ✓ |   |   |
| Manage application settings 	     | ✓ | ✓ | ✓ |   |   |
| Manage repositories	             | ✓ | ✓ | ✓ |   |   |
| Manage integrations	             | ✓ | ✓ | ✓ |   |   |
| Manage bundles    	             | ✓ | ✓ | ✓ |   |   |
| Manage team 	                     | ✓ | ✓ |   |   |   |
| Manage servers	                 | ✓ | ✓ |   |   |   |
| Manage organization	             | ✓ |   |   |   |   |
| Manage billing    	             | ✓ |   |   |   | &nbsp; |	 

Developers can view only resources used by applications they have access to

## Access to Applications and Instances 

By default all team members except unprivileged have access to a newly created applications. Optionally, you can restrict an application's access to certain team members. This access will be used by default for all newly created instances but you can override it during new instances creation.

Owners and administrators always have full access to all applications and instances