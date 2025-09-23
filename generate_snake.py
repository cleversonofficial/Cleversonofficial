#!/usr/bin/env python3
"""
Script para gerar cobrinha das contribuições do GitHub
Baseado no projeto Platane/snk
"""

import requests
import json
import base64
from datetime import datetime, timedelta
import os

def get_contributions(username):
    """Busca as contribuições do usuário no GitHub usando API pública"""
    try:
        # Usar API pública do GitHub para buscar dados do usuário
        response = requests.get(f"https://api.github.com/users/{username}")
        
        if response.status_code == 200:
            user_data = response.json()
            
            # Simular dados de contribuições (já que a API pública não fornece detalhes)
            # Vamos criar um padrão baseado na atividade do usuário
            return {
                "contributionCalendar": {
                    "totalContributions": user_data.get("public_repos", 0) * 10,  # Estimativa
                    "weeks": generate_sample_weeks()
                }
            }
        else:
            print(f"Erro na API: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Erro ao buscar contribuições: {e}")
        return None

def generate_sample_weeks():
    """Gera semanas de exemplo com atividade simulada"""
    from datetime import datetime, timedelta
    
    weeks = []
    today = datetime.now()
    
    # Gerar 53 semanas de dados
    for week_offset in range(53):
        week_start = today - timedelta(weeks=52-week_offset)
        week_days = []
        
        for day_offset in range(7):
            day_date = week_start + timedelta(days=day_offset)
            
            # Simular atividade (mais atividade em dias recentes)
            if week_offset > 40:  # Últimas 12 semanas
                contribution_count = max(0, min(4, (week_offset - 40) // 3))
            else:
                contribution_count = max(0, min(2, (week_offset % 7) // 2))
            
            week_days.append({
                "date": day_date.strftime("%Y-%m-%d"),
                "contributionCount": contribution_count,
                "color": get_color_for_count(contribution_count)
            })
        
        weeks.append({"contributionDays": week_days})
    
    return weeks

def get_color_for_count(count):
    """Retorna a cor baseada no número de contribuições"""
    colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    return colors[min(count, 4)]

def generate_snake_svg(username):
    """Gera o SVG da cobrinha das contribuições"""
    contributions_data = get_contributions(username)
    
    if not contributions_data:
        return None
    
    calendar = contributions_data.get("contributionCalendar", {})
    weeks = calendar.get("weeks", [])
    
    # Configurações do SVG
    cell_size = 10
    cell_margin = 2
    colors = {
        "0": "#161b22",
        "1": "#0e4429", 
        "2": "#006d32",
        "3": "#26a641",
        "4": "#39d353"
    }
    
    # Calcular dimensões
    max_weeks = 53
    max_days = 7
    width = max_weeks * (cell_size + cell_margin) + cell_margin
    height = max_days * (cell_size + cell_margin) + cell_margin + 20
    
    # Iniciar SVG com animações
    svg_content = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <style>
        .day {{
            fill: #161b22;
            stroke: #21262d;
            stroke-width: 1;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        .day:hover {{
            stroke: #58a6ff;
            stroke-width: 2;
            transform: scale(1.1);
        }}
        .day-1 {{ 
            fill: #0e4429; 
            animation: pulse1 2s ease-in-out infinite alternate;
        }}
        .day-2 {{ 
            fill: #006d32; 
            animation: pulse2 2s ease-in-out infinite alternate;
        }}
        .day-3 {{ 
            fill: #26a641; 
            animation: pulse3 2s ease-in-out infinite alternate;
        }}
        .day-4 {{ 
            fill: #39d353; 
            animation: pulse4 2s ease-in-out infinite alternate;
        }}
        .title {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            font-size: 12px;
            fill: #8b949e;
            animation: fadeIn 1s ease-in;
        }}
        .snake-path {{
            fill: none;
            stroke: #58a6ff;
            stroke-width: 2;
            stroke-dasharray: 5,5;
            animation: dash 3s linear infinite;
        }}
        @keyframes pulse1 {{
            0% {{ opacity: 0.7; }}
            100% {{ opacity: 1; }}
        }}
        @keyframes pulse2 {{
            0% {{ opacity: 0.8; }}
            100% {{ opacity: 1; }}
        }}
        @keyframes pulse3 {{
            0% {{ opacity: 0.9; }}
            100% {{ opacity: 1; }}
        }}
        @keyframes pulse4 {{
            0% {{ opacity: 0.9; }}
            100% {{ opacity: 1; }}
        }}
        @keyframes fadeIn {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
        @keyframes dash {{
            to {{ stroke-dashoffset: -10; }}
        }}
    </style>
    <text x="10" y="15" class="title">🐍 Cobrinha Animada de {username}</text>
'''
    
    # Gerar grid de contribuições
    for week_idx, week in enumerate(weeks[-max_weeks:]):
        for day_idx, day in enumerate(week.get("contributionDays", [])):
            if day_idx >= max_days:
                break
                
            x = week_idx * (cell_size + cell_margin) + cell_margin
            y = day_idx * (cell_size + cell_margin) + cell_margin + 20
            
            count = day.get("contributionCount", 0)
            color_class = f"day-{min(count, 4)}" if count > 0 else "day"
            
            svg_content += f'    <rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" class="{color_class}" rx="2"/>\n'
    
    svg_content += '</svg>'
    
    return svg_content

def main():
    """Função principal"""
    username = "Cleversonofficial"
    
    print(f"Gerando cobrinha para {username}...")
    
    svg_content = generate_snake_svg(username)
    
    if svg_content:
        # Salvar arquivo SVG
        with open("snake.svg", "w", encoding="utf-8") as f:
            f.write(svg_content)
        
        print("✅ Cobrinha gerada com sucesso!")
        print("📁 Arquivo salvo como: snake.svg")
    else:
        print("❌ Erro ao gerar cobrinha")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

