#!/bin/bash

# Script che mostra tutti i test disponibili per l'agente

# Colori
BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${BOLD}${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${BLUE}║        TEST DISPONIBILI - Medical Research Assistant Agent         ║${NC}"
echo -e "${BOLD}${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Script Python
echo -e "${BOLD}${CYAN}📝 SCRIPT DI TEST PYTHON:${NC}"
echo ""

if [ -f "test_agente.py" ]; then
    echo -e "  ${GREEN}✓${NC} test_agente.py"
    echo -e "    ${YELLOW}→${NC} Test base dell'agente (senza server)"
    echo -e "    ${YELLOW}→${NC} Comando: ${BOLD}python test_agente.py${NC}"
    echo ""
fi

if [ -f "test_agente_api.py" ]; then
    echo -e "  ${GREEN}✓${NC} test_agente_api.py"
    echo -e "    ${YELLOW}→${NC} Test completo con server API"
    echo -e "    ${YELLOW}→${NC} Comando: ${BOLD}python test_agente_api.py${NC}"
    echo ""
fi

if [ -f "esempio_uso_agente.py" ]; then
    echo -e "  ${GREEN}✓${NC} esempio_uso_agente.py"
    echo -e "    ${YELLOW}→${NC} Esempi interattivi di utilizzo"
    echo -e "    ${YELLOW}→${NC} Comando: ${BOLD}python esempio_uso_agente.py${NC}"
    echo ""
fi

# Script Bash
echo -e "${BOLD}${CYAN}🔧 SCRIPT BASH:${NC}"
echo ""

if [ -f "testa_agente.sh" ]; then
    echo -e "  ${GREEN}✓${NC} testa_agente.sh"
    echo -e "    ${YELLOW}→${NC} Script unificato per tutti i test"
    echo -e "    ${YELLOW}→${NC} Comandi:"
    echo -e "      ${BOLD}./testa_agente.sh base${NC}    - Test base"
    echo -e "      ${BOLD}./testa_agente.sh api${NC}     - Test API"
    echo -e "      ${BOLD}./testa_agente.sh manuale${NC} - Server per test manuali"
    echo ""
fi

# Documentazione
echo -e "${BOLD}${CYAN}📚 GUIDE E DOCUMENTAZIONE:${NC}"
echo ""

if [ -f "GUIDA_RAPIDA_TEST.md" ]; then
    echo -e "  ${GREEN}✓${NC} GUIDA_RAPIDA_TEST.md"
    echo -e "    ${YELLOW}→${NC} Guida rapida con esempi pratici"
    echo ""
fi

if [ -f "README_TEST_AGENTE.md" ]; then
    echo -e "  ${GREEN}✓${NC} README_TEST_AGENTE.md"
    echo -e "    ${YELLOW}→${NC} README completo sui test"
    echo ""
fi

if [ -f "TESTING_INDEX.md" ]; then
    echo -e "  ${GREEN}✓${NC} TESTING_INDEX.md"
    echo -e "    ${YELLOW}→${NC} Indice completo di tutte le risorse"
    echo ""
fi

if [ -f "medical_agent/README.md" ]; then
    echo -e "  ${GREEN}✓${NC} medical_agent/README.md"
    echo -e "    ${YELLOW}→${NC} Documentazione completa del medical agent"
    echo ""
fi

# Test Pytest
echo -e "${BOLD}${CYAN}🧪 TEST AUTOMATICI (PYTEST):${NC}"
echo ""

if [ -d "medical_agent/tests" ]; then
    echo -e "  ${GREEN}✓${NC} medical_agent/tests/"
    echo -e "    ${YELLOW}→${NC} Test suite completa con pytest"
    echo -e "    ${YELLOW}→${NC} Comando: ${BOLD}cd medical_agent && pytest tests/ -v${NC}"
    echo ""
fi

# Quick Start
echo -e "${BOLD}${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${BLUE}║                           QUICK START                              ║${NC}"
echo -e "${BOLD}${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BOLD}Test più veloce (consigliato per iniziare):${NC}"
echo -e "  ${GREEN}$${NC} ${BOLD}python test_agente.py${NC}"
echo ""

echo -e "${BOLD}Test completo con API:${NC}"
echo -e "  ${GREEN}$${NC} ${BOLD}python test_agente_api.py${NC}"
echo ""

echo -e "${BOLD}Oppure usa lo script bash:${NC}"
echo -e "  ${GREEN}$${NC} ${BOLD}./testa_agente.sh base${NC}"
echo ""

echo -e "${BOLD}Per vedere esempi d'uso:${NC}"
echo -e "  ${GREEN}$${NC} ${BOLD}python esempio_uso_agente.py${NC}"
echo ""

# Footer
echo -e "${BOLD}${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}${BLUE}║  Per maggiori dettagli, consulta: GUIDA_RAPIDA_TEST.md           ║${NC}"
echo -e "${BOLD}${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}💡 Suggerimento:${NC} Esegui ${BOLD}./testa_agente.sh help${NC} per vedere tutte le opzioni"
echo ""
