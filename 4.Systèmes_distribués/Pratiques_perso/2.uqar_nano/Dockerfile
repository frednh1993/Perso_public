# On debute a partir d'une image nginx qui est un logiciel de Server Web sous
# Linux.
FROM nginx:alpine

# Commande (apk add nano) linux pour installer Nano qui est un text editor 
# pour ecrire et mettre a jour des fichiers sous Linux.
RUN apk add nano

# Copie du contenu de notre repertoire file dans le repertoire nginx pour la
# diffusion de page web (imp : UTILISER PORT 80 !).
COPY file/. /usr/share/nginx/html