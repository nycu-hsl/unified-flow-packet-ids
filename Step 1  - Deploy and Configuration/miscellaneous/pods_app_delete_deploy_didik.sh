#!/bin/bash


dep_status=$(kubectl get deployments.apps)
if [ $dep_status = "No resources found in default namespace." ]; then

	echo ""
	echo ""
	echo "============================="
	echo " Install Google Microservice"
	echo "============================="
	kubectl apply -f /home/hsl/APM.app/microservices-demo/release/kubernetes-manifests.yaml

	echo ""
	echo ""
	echo "============================="
	echo "  Installing socialnetwork"
	echo "============================="
	helm install socialnetwork /home/hsl/APM.app/DeathStarBench/socialNetwork/helm-chart/socialnetwork/ --set-string global.imagePullPolicy=Always --set global.mongodb.sharding.enabled=false,global.mongodb.standalone.enabled=true --timeout 10m0s


	echo ""
	echo ""
	echo "============================="
	echo "Adding External Access for SN"
	echo "============================="
	kubectl expose deployment nginx-thrift --type=NodePort --name=nginx-thrift-6455574474-pwrf6 service "nginx-thrift" exposed


	kubectl get  svc > pods_services_$(date +"%Y%m%d-%H%M")

else
	echo "============================="
	echo "     Deleting deployment"
	echo "============================="
	kubectl delete deployments adservice cartservice checkoutservice compose-post-service currencyservice emailservice frontend home-timeline-redis home-timeline-service jaeger media-frontend media-memcached media-mongodb media-service nginx-thrift paymentservice post-storage-memcached post-storage-mongodb post-storage-service productcatalogservice recommendationservice redis-cart shippingservice social-graph-mongodb social-graph-redis social-graph-service text-service unique-id-service url-shorten-memcached url-shorten-mongodb url-shorten-service user-memcached user-mention-service user-mongodb user-service user-timeline-mongodb user-timeline-redis user-timeline-service loadgenerator dvwa mariadb
  kubectl delete namespaces dvwa

	echo ""
	echo ""
	echo "============================="
	echo "        Deleting pods"
	echo "============================="
	kubectl delete pod helloworld-python helloworld-python-access-pod setup-collection-sharding-hook

	echo ""
	echo ""
	echo "============================="
	echo "      Deleting services"
	echo "============================="
	kubectl delete svc adservice cartservice checkoutservice compose-post-service currencyservice emailservice emailme-timeline-redis frontend frontend-external home-timeline-service jaeger nginx-thrift nginx-thrift-6455574474-pwrf6 paymentservice post-storage-memcached post-ss-cart productcatalogservice recommendationservice redis-cart shippingservice social-graph-mongodb social-graph-redis social-graph-service text-service unique-ied user-mention-service user-mongodb user-service user-timeline-mongodb user-timeline-redis user-timeline dvwa mariadb

	echo ""
	echo ""
	echo "============================="
	echo "   Uninstall socialnetwork"
	echo "============================="
	helm uninstall socialnetwork

	echo ""
	echo ""
	echo "============================="
	echo " Install Google Microservice"
	echo "============================="
	kubectl apply -f /home/hsl/APM.app/microservices-demo/release/kubernetes-manifests.yaml

  echo ""
	echo ""
	echo "============================="
	echo " Install Damn Vulnerable Web Application"
	echo "============================="
	kubectl apply -f /home/hsl/APM-ITRI/dvwa_deployment/01-mariadb.yaml
	kubectl apply -f /home/hsl/APM-ITRI/dvwa_deployment/02-app.yaml

	echo ""
	echo ""
	echo "============================="
	echo "  Installing socialnetwork"
	echo "============================="
	helm install socialnetwork /home/hsl/APM.app/DeathStarBench/socialNetwork/helm-chart/socialnetwork/ --set-string global.imagePullPolicy=Always --set global.mongodb.sharding.enabled=false,global.mongodb.standalone.enabled=true --timeout 10m0s


	echo ""
	echo ""
	echo "============================="
	echo "Adding External Access for SN"
	echo "============================="
	kubectl expose deployment nginx-thrift --type=NodePort --name=nginx-thrift-6455574474-pwrf6 service "nginx-thrift" exposed


	kubectl get  svc > pods_services_$(date +"%Y%m%d-%H%M")


fi

