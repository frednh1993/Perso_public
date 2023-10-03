package main
import ("fmt"
"net/http"
"github.com/gorilla/mux"
"log"
_ "github.com/go-sql-driver/mysql"
"database/sql"
"encoding/json"
"os"
)
type etudiant struct {
	ID  int    `json:"Id"`
	Nom string `json:"Nom"`
}
//Variables pour la connexion session.
var databaseUser string
var databasePassword string


func main() {
	fmt.Println("Starting Web Service")

	databaseUser = os.Getenv("DB_USER")
	databasePassword = os.Getenv("DB_PASSWORD")
	//Routeur qui ecoute.
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/health", healthHandler)
	router.HandleFunc("/etudiants", etudiantHandler)
	http.ListenAndServe(":8080", router)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("healthHandler called")
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}

func etudiantHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("etudiantHandler called")
	w.Header().Set("Content-Type", "application/json")
	// db, err := sql.Open("mysql", "root:pass@tcp(mysql:3306)/uqar")
	db, err := sql.Open("mysql", databaseUser+":"+databasePassword+"@tcp(mysql:3306)/uqar")
	//defer: apres que la fonction sera termine.
	if err != nil {
		log.Fatal(err)
	}

	defer db.Close()
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

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(etudiantList)
}
