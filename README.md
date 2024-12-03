# Projet Architecture Logicielle - MkReservation
### Mayatta Ndiaye, Killian Marty

## Introduction 

Ce logiciel est un Proof of Concept d'un projet de SaaS de réservation de rendez-vous.
Il a été réalisé dans le cadre du cours d'Architecture des logiciels à l'Université du Québec à Chicoutimi.

## Installation

### 1. Installer docker et docker-compose

```bash
sudo apt install -y docker docker-compose
```

### 2. Cloner le repository

```bash
git clone https://github.com/killianmarty/Projet_architecture

cd Projet_architecture
```

### 3. Construire les conteneurs docker

```bash
docker-compose build
```

### 4. Lancer les conteneurs docker

```bash
docker-compose up
```

### 5. Accèder à MkRéservation

Il est maintenant possible d'accèder à MkRéservation à l'adresse http://127.0.0.1:8080/.

## Monitorer le logiciel

Une composante de monitoring (portainer) est inclue dans le logiciel, elle est accessible à l'adresse http://127.0.0.1:9000/.