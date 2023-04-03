package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/Shopify/sarama"
	_ "github.com/go-sql-driver/mysql"
	"github.com/gorilla/mux"
)

type etudiant struct {
	ID  int    `json:"Id"`
	Nom string `json:"Nom"`
}

var databaseUser string
var databasePassword string

var etudiantProducer sarama.SyncProducer

func main() {
	fmt.Println("Starting Web Service")

	etudiantProducer = newKafkaProducer()
	defer etudiantProducer.Close()

	databaseUser = os.Getenv("DB_USER")
	databasePassword = os.Getenv("DB_PASSWORD")

	router := mux.NewRouter().StrictSlash(true)

	router.HandleFunc("/health", healthHandler)
	router.HandleFunc("/etudiants", etudiantsGetHandler).Methods("GET")
	router.HandleFunc("/etudiants", etudiantsPostHandler).Methods("POST")

	http.ListenAndServe(":8080", router)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("healthHandler called")
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}

func etudiantsGetHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("etudiantsGetHandler called")
	db, err := sql.Open("mysql", databaseUser+":"+databasePassword+"@tcp(mysql:3306)/uqar")
	defer db.Close()

	if err != nil {
		log.Fatal(err)
	}

	res, err := db.Query("SELECT * FROM etudiants")
	defer res.Close()

	var etudiantList []etudiant
	for res.Next() {

		var currentEtudiant etudiant
		err := res.Scan(&currentEtudiant.ID, &currentEtudiant.Nom)

		if err != nil {
			log.Fatal(err)
		}

		etudiantList = append(etudiantList, currentEtudiant)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(etudiantList)
}

func etudiantsPostHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("etudiantsPostHandler called")
	w.Header().Set("Content-Type", "application/json")

	var etudiant etudiant
	// decode la requete http pour en extraire les infos.
	decoder := json.NewDecoder(r.Body)
	if err := decoder.Decode(&etudiant); err != nil {
		fmt.Println("etudiantsPostHandler error: ", err.Error())
		w.WriteHeader(http.StatusBadRequest)
		return
	}
	defer r.Body.Close()
	// producer pas besoin de donner un nom.
	partition, offset, err := etudiantProducer.SendMessage(&sarama.ProducerMessage{
		Topic: "uqar",
		Value: sarama.StringEncoder(etudiant.Nom),
	})

	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprintf(w, "Failed to store your data:, %s", err)
	} else {
		fmt.Fprintf(w, "Etudiant : /%s added to partition : /%d with offset : /%d", etudiant.Nom, partition, offset)
	}
}

func newKafkaProducer() sarama.SyncProducer {
	brokerList := []string{"kafka-0.kafka.default.svc.cluster.local:9092", "kafka-1.kafka.default.svc.cluster.local:9092", "kafka-2.kafka.default.svc.cluster.local:9092"}
	config := sarama.NewConfig()
	config.Producer.Return.Successes = true

	producer, err := sarama.NewSyncProducer(brokerList, config)
	if err != nil {
		log.Fatalln("Failed to start Sarama producer:", err)
	}

	return producer
}