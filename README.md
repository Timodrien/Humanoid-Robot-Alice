# Alice — Humanoider VR-Telepresence-Roboter 🤖

Ein humanoider Roboter, entwickelt für die Fernsteuerung mittels Virtual-Reality-(VR)-Headsets. Dient als vielseitiger Avatar mit Potenzial zur zukünftigen Integration in das [LESS-Projekt](#).

![Alice in Aktion](docs/images/alice_hero.jpg)
<!-- Bild/GIF hier einfügen, sobald vorhanden -->

## Features

- **VR-Integration** — Steuerung über ein Meta Quest 3S Headset, Umgebungswahrnehmung in Echtzeit über Kamera
- **Inside Out Body Tracking (IOBT)** — Arme und Beine bewegen sich synchron mit den Nutzerbewegungen
- **Erschwingliches Design** — Version 2 nutzt einen Raspberry Pi 3A+ für Grundfunktionen bei niedrigen Kosten
- **Kopfsteuerung über Headset** — Kopfbewegungen des Nutzers werden erfasst und auf Alice übertragen
- **Echtzeit-Bildübertragung** — Live-Kamerabild direkt auf das VR-Headset

## Hardware

| Komponente | Details |
|---|---|
| Compute | Raspberry Pi 3A+ |
| VR-Headset | Meta Quest 3S |
| Tracking | Inside Out Body Tracking (IOBT) <!-- Sensoren/Methode ergänzen --> |
| Kamera | <!-- Modell ergänzen --> |
| Aktuatoren | <!-- Servos/Motoren für Arme & Beine --> |
| Stromversorgung | <!-- Akku-Typ, Laufzeit --> |

## Software-Stack

- **Steuerung/Firmware:** <!-- z. B. Python auf dem Pi -->
- **VR-Anbindung:** <!-- z. B. Unity/OpenXR für Meta Quest 3S -->
- **Bildübertragung:** <!-- Streaming-Protokoll ergänzen -->
- **Tracking-Pipeline:** IOBT-Datenverarbeitung → Motoransteuerung

## Setup

```bash
git clone https://github.com/<dein-name>/alice.git
cd alice

# Python-Abhängigkeiten
pip install -r requirements.txt

# Auf dem Raspberry Pi 3A+ ausführen
# <Startbefehl ergänzen>
```

Konfiguration (WLAN-Zugangsdaten, API-Keys etc.) liegt in `config.example.h` — kopieren nach `config.h` und mit eigenen Werten befüllen. `config.h` ist in `.gitignore` und wird nicht mit hochgeladen.

## Projektstruktur

```
alice/
├── src/
│   ├── control/         # Bewegungssteuerung, IOBT-Verarbeitung
│   ├── vr-bridge/        # Verbindung zum VR-Headset
│   └── streaming/        # Kamera-/Bildübertragung
├── hardware/              # CAD/STL-Dateien, Wiring-Diagramme
├── docs/images/           # Bilder & GIFs für README
├── config.example.h
└── README.md
```

## Verwandte Projekte

- [LESS-Projekt](#) — geplante zukünftige Integration von Alice als Avatar
- Smartphone-App zur Steuerung von Alice, Fox und SMV

## Roadmap / Ideen

<!-- optional: geplante Erweiterungen, offene TODOs -->

## Lizenz

<!-- MIT o.ä. einfügen, oder Zeile entfernen wenn keine Lizenz gewünscht -->
