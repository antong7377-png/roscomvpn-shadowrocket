# RoscomVPN Routing для Shadowrocket

Хирургический роутинг для iOS на основе [hydraponique/roscomvpn-routing](https://github.com/hydraponique/roscomvpn-routing).

## Быстрая установка

1. Откройте **Shadowrocket**
2. **Config** → **+** → **Download from URL**
3. Вставьте:
```
https://raw.githubusercontent.com/antong7377-png/roscomvpn-shadowrocket/main/roscomvpn.conf
```
4. Добавьте свой прокси-сервер
5. Включите VPN

## Что делает

| Действие | Что попадает |
|----------|-------------|
| 🔴 REJECT | Телеметрия Windows, торренты, реклама |
| 🔵 PROXY | YouTube, Telegram, Google Play, GitHub |
| 🟢 DIRECT | Рунет, банки, VK, Яндекс, Steam, Apple, игры |
| 🌍 GEOIP,RU | Все российские IP → DIRECT |

## Авто-обновление

GitHub Actions конвертирует правила из upstream-репо **ежедневно** в 06:00 UTC.

Shadowrocket обновляет подписку при запуске (или по расписанию).

## Структура

- `roscomvpn.conf` — основной конфиг Shadowrocket
- `*.list` — RULE-SET файлы (конвертированы из v2fly формата)
- `convert.py` — скрипт конвертации
- `.github/workflows/update-rules.yml` — авто-обновление

## Источник

Все правила берутся из [hydraponique/roscomvpn-routing](https://github.com/hydraponique/roscomvpn-routing).
