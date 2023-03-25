package main
import ("fmt"
"net/http"
"github.com/gorilla/mux"
"log"
_ "github.com/go-sql-driver/mysql"
"database/sql"
"encoding/json"
)


type etudiant struct {
	ID  int    `json:"Id"`
	Nom string `json:"Nom"`
}


// API port 80, route /health et route /etudiant
func main() {
	fmt.Println("Starting Web Service")

	router := mux.NewRouter().StrictSlash(true)

	router.HandleFunc("/health", healthHandler)
	router.HandleFunc("/etudiant", etudiantHandler)
	http.ListenAndServe(":80", router)
}


// Endpoint de /health
func healthHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("healthHandler called")
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
}


// Endpoint de /etudiant
func etudiantHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("etudiantHandler called")
	w.Header().Set("Content-Type", "application/json")

	// MuSQL, root:pass@tcp(mysql:3306)/uqar
	db, err := sql.Open("mysql", "root:pass@tcp(mysql:3306)/uqar")
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

	// Reponse de la requete
	json.NewEncoder(w).Encode(etudiantList)
	w.WriteHeader(http.StatusOK)
}