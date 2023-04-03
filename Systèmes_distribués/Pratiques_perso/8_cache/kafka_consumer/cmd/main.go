package main

import (
	"context"
	"database/sql"
	"fmt"
	"log"
	"os"

	"github.com/Shopify/sarama"
	_ "github.com/go-sql-driver/mysql"
)

type etudiant struct {
	ID  int    `json:"Id"`
	Nom string `json:"Nom"`
}

var databaseUser string
var databasePassword string

func main() {
	fmt.Println("Starting kafka consumer")

	client := newKafkaClient()
	defer client.Close()

	databaseUser = os.Getenv("DB_USER")
	databasePassword = os.Getenv("DB_PASSWORD")

	for {
		// `Consume` should be called inside an infinite loop, when a
		// server-side rebalance happens, the consumer session will need to be
		// recreated to get the new claims
		if err := client.Consume(context.Background(), []string{"uqar"}, &Consumer{}); err != nil {
			log.Panicf("Error from consumer: %v", err)
		}
	}
}

func newKafkaClient() sarama.ConsumerGroup {
	brokerList := []string{"kafka-0.kafka.default.svc.cluster.local:9092", "kafka-1.kafka.default.svc.cluster.local:9092", "kafka-2.kafka.default.svc.cluster.local:9092"}
	config := sarama.NewConfig()

	consumer, err := sarama.NewConsumerGroup(brokerList, "uqar.etudiant.consumer", config)
	if err != nil {
		log.Panicf("Error creating consumer group client: %v", err)
	}

	return consumer
}

type Consumer struct {
}

// Setup is run at the beginning of a new session, before ConsumeClaim
func (consumer *Consumer) Setup(sarama.ConsumerGroupSession) error {
	return nil
}

// Cleanup is run at the end of a session, once all ConsumeClaim goroutines have exited
func (consumer *Consumer) Cleanup(sarama.ConsumerGroupSession) error {
	return nil
}

// ConsumeClaim must start a consumer loop of ConsumerGroupClaim's Messages().
func (consumer *Consumer) ConsumeClaim(session sarama.ConsumerGroupSession, claim sarama.ConsumerGroupClaim) error {
	for message := range claim.Messages() {
		log.Printf("Message claimed: value = %s, timestamp = %v, topic = %s", string(message.Value), message.Timestamp, message.Topic)
		addEtudiant(string(message.Value))
		session.MarkMessage(message, "")
	}

	return nil
}

func addEtudiant(name string) {
	db, err := sql.Open("mysql", databaseUser+":"+databasePassword+"@tcp(mysql:3306)/uqar")
	defer db.Close()

	if err != nil {
		log.Fatal(err)
	}

	sqlStatement := "INSERT INTO etudiants (id, nom) VALUES (NULL, '" + name + "')"
	_, err = db.Exec(sqlStatement)
	if err != nil {
		panic(err)
	}
}