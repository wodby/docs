# Continuous Integration and Delivery

There are 2 ways to organize CI/CD workflow with Wodby depending on what stack you're using:
 
## 1. Managed Stack
 
TBD
 
## 2. Custom Stack

Prerequisites:

1. CI tool to perform the build (Jenkins, GitLab CI, Travis CI, CircleCI, etc) 
2. Private docker registry (self-hosted Docker registry, Docker Hub, Quay, GCR, etc)

How it works:

1. [Create custom stack](../stacks/template.md) with your docker images
2. At least one image will have codebase inside of it, this image should be hosted in a private docker registry
3. In your CI tool you should pull this image and copy your build with codebase
4. Push the updated image with codebase to a registry   
5. Deploy your new image using one of these methods:
    1. Image has a new tag: update your stack and instance from Wodby dashboard manually 
    2. Image has the same tag: request our [API](../api/README.md) method *Deploy stacks by image name*. Wodby will automatically redeploy all instances that have specified image:tag in their stacks
