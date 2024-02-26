
Sobre endpoints de stages

- Una enginyeria que té diversos usuaris. Cada usuari pot veure tots els projectes de l'enginyeria o s'ha de poder compartimentar?


Tres tipus usuari:
- Enginyeria
- OV
- Unauthenticated User (E.g. Web)

Endpoint públic (per l'usuari Web que de fet no és unusuari):
- Campanya
- Stats

Model:
- Enginyeria 1-1 User
- Enginyeria 1-n Projecte
- Projecte 1-n Stages

Client serà la persona usuaria a la OV

Endpoints que cal gestionar amb permisos:
- Project
- Stages
Retorna l'estat que demani per url (per exemple. prereport) del projecte que toqui. El filtre el fa el serializer
serializer_class = PrereportStageSerializer
- Events (forma part de som renkonto i està aturat de moment, deixar apart, cal deshabilitar-lo a producció)
Si sóc OV només puc demanar projectes a partir d'un DNi, no tornar-los tots.
Enginyeria (usuari) ha de tenir accés només als seus projectes


Endpoints sense permisos:
- Campaign
- Stats
