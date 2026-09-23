#!/bin/bash

# Script per testare l'agente Medical Research Assistant
# Uso: ./testa_agente.sh [base|api|manuale]

set -e

# Colori per output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}   TEST AGENTE MEDICAL RESEARCH     ${NC}"
echo -e "${BLUE}=====================================${NC}"
echo ""

# Funzione per mostrare l'uso
show_usage() {
    echo "Uso: $0 [base|api|manuale|help]"
    echo ""
    echo "Opzioni:"
    echo "  base      - Test base dell'agente (senza server)"
    echo "  api       - Test completo con server API"
    echo "  manuale   - Avvia il server per test manuali"
    echo "  help      - Mostra questo messaggio"
    echo ""
    echo "Se non specifichi un'opzione, verrà eseguito il test base."
    exit 0
}

# Funzione test base
test_base() {
    echo -e "${GREEN}Esecuzione test base...${NC}"
    echo ""
    python test_agente.py
}

# Funzione test API
test_api() {
    echo -e "${GREEN}Esecuzione test API...${NC}"
    echo ""
    echo -e "${YELLOW}Il server verrà avviato automaticamente.${NC}"
    echo -e "${YELLOW}Premi Ctrl+C per terminare il server quando hai finito.${NC}"
    echo ""
    python test_agente_api.py
}

# Funzione test manuale
test_manuale() {
    echo -e "${GREEN}Avvio server per test manuali...${NC}"
    echo ""
    echo -e "${YELLOW}Il server sarà disponibile su: http://localhost:5000${NC}"
    echo ""
    echo "Puoi testarlo con:"
    echo "  curl http://localhost:5000/health"
    echo ""
    echo "  curl -X POST http://localhost:5000/api/ask \\"
    echo "    -H 'Content-Type: application/json' \\"
    echo "    -d '{\"question\": \"Cos'\''è il diabete?\"}'"
    echo ""
    echo -e "${YELLOW}Premi Ctrl+C per terminare il server.${NC}"
    echo ""
    cd medical_agent
    python backend/app.py
}

# Verifica argomenti
case "${1:-base}" in
    base)
        test_base
        ;;
    api)
        test_api
        ;;
    manuale)
        test_manuale
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo -e "${YELLOW}Opzione sconosciuta: $1${NC}"
        echo ""
        show_usage
        ;;
esac
