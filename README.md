# monitor-app-kubernetes 
**App Info**: This simple application allows you to upload the file and monitors those uploaded file.
A guide on deploying this simple server's file monitoring app which uses flask and postgres. In this setup, deployment is handled via argocd. argoCD lets you to sync your application from the remote repository. Specify a directory where your kubernetes manifests file is located at. 

**Why Kustomize ?**  
You do not need kustomize setup if your goal is to simply deploy the application using kubernetes manifests(plain yaml) only. Your application will sync only when it sees a change in your deployment directory. So you need to make a change in kubernetes manifests file whenever a new image is deployed in your container registry with different image tag and if you always use the latest image tag then argocd won't be able to sync even when you push a new image using latest image tag in your container registry.

So what you could do is install argocd-image-updater in your current kubernetes cluster where argocd is installed. Argo CD Image Updater is a tool to automatically update the container images of Kubernetes workloads which are managed by Argo CD. In a nutshell, it will track image versions specified by annotations on the Argo CD Application resources and update them by setting parameter overrides using the Argo CD API.  

Currently it will only work with applications that are built using Kustomize or Helm tooling. Applications built from plain YAML or custom tools are not supported yet (and maybe never will). That is why kustomize is implemented.  


---

## Directory guide
- **monitor-app**: Flask application with Dockerfile to build the Docker image. This app monitors the information of uploaded file from the dashboard and provides the information of uploaded file in the dashboard. 
- **flask-kube**: Kubernetes manifests file to create Flask deployment with services and configmap with a kustomize setup. 
- **postgres-kube**: Kubernetes manifests file to create Stateful postgres DB application with service, configmap, persistent volume, and persistent volume claim

---

## Prerequisite
- Docker 
- Kubernetes cluster 
- argoCD
- argocd-image-updater

For testing purpose you may use Docker Desktop in which Kubernetes is installed.

---

## Build Docker Image
Building a docker image is completely a Continuous Integration process for packaging an application. Pushing it to your container registry is creating an artifacts to deploy. Hence, it is better to seggragate this application building part in different repo where you could write your own Jenkinsfile to build the image and push it to the container registry.
Steps to build the docker image and push to your container registry(for now docker registry):
1. First clone this repository and change the application directory.
2. Build docker image (`docker build -t ${tagname} .`)
3. Push image to your dockerhub account. (`docker push ${tagname}`)
   
Note the image tag name here. This image tag name will be used in Kubernetes manifest file for flask.  
cmdline instructions to build and push docker image:  

```
cd monitor-app
docker build -t sushanku/flask-monitor-app:latest .
docker push sushanku/flask-monitor-app:latest
```

---

## Deploy flask app in your Kubernetes cluster
This flask app is first built with Docker and pushed it to the public dockerhub registry. Then, Kubernetes will pull the docker image from the dockerhub and create a deployment pods.
This deployment is handled with Kustomize setup. It has dev and production environment overlay setup. Patches include different service type and different resource limits.  
Dev setup will deploy the application with serviceType as a nodePort and limited resources.  
Production setup will deploy the application with serviceType as a loadbalancer and limited resources. You may learn more about exposing your services using different ports and service type here. [Networking Service](https://kubernetes.io/docs/concepts/services-networking/service/)  
This app also needs the environment variables like Database host, port, username, password etc which is handled by configMap resources. configMap allows you to decouple your hardcorded environment variable in the application code.  
For username, password or any critical information it is best to use Kuberenetes secret resource or Hashicorp vault.  


**Note:** Do not forget to change the volume path in postgres-volume.yaml.  
Make sure the directory exists. Here is the reference  `path: "/Users/example/Desktop/kubedata"`. Change this path to match your local directory.  

Lets create the flask config, service and deployment 
```
kubectl apply -f flask-kube
```
The above kubectl apply command will apply all the manifests file in flask-kube directory.

---

## Deploy postgres DB in your Kubernetes cluster
This postgress app uses a statefulset controller to deploy the stateful pods which have the persistent storage and a network.  
  
This app also needs the environment variables like Database username and password etc which is handled by configMap resources.Same username and password info should be given to the configMap of the flask. configMap allows you to decouple your hardcorded environment variable in the application code. For username, password or any critical information it is best to use Kuberenetes secret resource or Hashicorp vault.  
  
To expose the postgres DB within a cluster, postgres service manifest file is created. This will create a service accessible within a cluster by a DNS name `postgres`. This DNS name is then fed into the Flask deployment which needs to know the DB_HOST as a environment variable.  
  
A PersistentVolume (PV) is a piece of storage in your cluster that helps to persist your container database to your local storage.For that you need to have a persistent volume and persistent volume claim. You may also use different types of other storage. Learn more about pv and pvc  [persistent-volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
  
Lets create the postgres pv, pvc, config, service and deployment 
```
kubectl apply -f flask-postgres
```
The above kubectl apply command will apply all the manifests file in postgres-kube directory.

---

## Endpoints
If you are using production environment, port is `5000` and for dev environment, port is `30007`
- **sign up**: http://localhost:5000/register  
  Sign Up page
- **login**: http://localhost:5000/login  
  Login page
- **file list**: http://localhost:5000/file_list.html  
  Page from where you can upload the file. This same page will display the uploaded file information(name, filesize, filetype, action to delete the file)
- **dashboard**: http://localhost:5000/dashboard.html  
  Dashboard where uploaded file count will be displayed on the basis of daily, weekly, monthly.

---

## TO DO's
These are the few suggestions for the enhancement of this application
- You may use kuberenetes resource `secret` for your DB username and DB password both in flask and postgres or You may use Hashicorp vault.
- Make a helm charts of this application and deploy it using helm.
