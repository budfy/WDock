# WDock - Windows Dock Application
# WDock - Застосунок Док-панелі для Windows

[English](#english) | [Українська](#українська)

---

## English

A modern, customizable dock panel for Windows with advanced features and smooth animations.

### Features

- **Adaptive Icons**: 48x48px icons with hover effects
- **Flexible Positioning**: Attach to any screen edge (top, bottom, left, right)
- **Smart Grouping**: Drag shortcuts together to create groups
- **Intelligent Auto-Hide**: Automatically hide during fullscreen applications
- **Theme Support**: Dark/light themes synchronized with Windows
- **Smooth Animations**: Fluid appearance, hiding, and group expansion effects
- **Multi-Monitor Support**: Works seamlessly across multiple displays
- **Low Memory Usage**: Optimized to use less than 50MB RAM
- **System Tray Integration**: Run in background with tray controls
- **Registry Integration**: Auto-startup with Windows support
- **Comprehensive Settings**: Full configuration through settings window

### Installation

#### From Source
1. Install Python 3.8 or higher
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python main.py`

#### Portable Version
1. Download the portable ZIP from releases
2. Extract to desired location
3. Run `WDock.exe`

#### Windows Installer
1. Download the installer from releases
2. Run the setup file
3. Follow installation wizard

### Usage

1. **Adding Icons**: Drag .exe files or .lnk shortcuts onto the dock
2. **Creating Groups**: Drag one icon onto another to create a group
3. **Positioning**: Right-click the dock → "Attach to" → Choose edge
4. **Settings**: Right-click → "Settings" for full configuration
5. **Auto-Hide**: Enable in settings for automatic hiding

### System Requirements

- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 50MB free disk space
- .NET Framework 4.7.2 or higher

### Building from Source

```bash
# Install build dependencies
pip install pyinstaller

# Build executable and installer
python build.py
```

### Project Structure

```
WDock/
├── main.py                    # Application entry point
├── build.py                   # Build script for distribution
├── requirements.txt           # Python dependencies
├── src/                      # Source code
│   ├── core/                # Core application logic
│   │   ├── config_manager.py    # Configuration management
│   │   ├── dock_window.py       # Main dock window
│   │   └── system_tray.py       # System tray integration
│   ├── ui/                  # User interface components
│   │   ├── icon_widget.py       # Icon widgets
│   │   ├── group_widget.py      # Group widgets
│   │   ├── settings_window.py   # Settings dialog
│   │   └── about_window.py      # About dialog
│   └── utils/               # Utility modules
│       ├── drag_drop.py         # Drag & drop functionality
│       ├── startup_manager.py   # Windows startup integration
│       ├── performance.py       # Performance monitoring
│       └── multi_monitor.py     # Multi-monitor support
├── tests/                    # Unit tests
├── assets/                   # Icons and images
└── docs/                     # Documentation
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### License

© WDock Project. All rights reserved.

---

## Українська

Сучасна, налаштовувана док-панель для Windows з розширеними функціями та плавними анімаціями.

### Можливості

- **Адаптивні Іконки**: Іконки 48x48px з ефектами наведення
- **Гнучке Позиціонування**: Прикріплення до будь-якого краю екрана (верх, низ, ліво, право)
- **Розумне Групування**: Перетягніть ярлики разом для створення груп
- **Інтелектуальне Автоприховування**: Автоматичне приховування під час повноекранних програм
- **Підтримка Тем**: Темна/світла теми синхронізовані з Windows
- **Плавні Анімації**: Плавна поява, приховування та розгортання груп
- **Підтримка Кількох Моніторів**: Бездоганна робота на кількох дисплеях
- **Низьке Використання Пам'яті**: Оптимізовано для використання менше 50МБ ОЗП
- **Інтеграція Системного Трею**: Робота у фоні з елементами керування в треї
- **Інтеграція з Реєстром**: Підтримка автозапуску з Windows
- **Повні Налаштування**: Повна конфігурація через вікно налаштувань

### Встановлення

#### З Вихідного Коду
1. Встановіть Python 3.8 або вищий
2. Встановіть залежності: `pip install -r requirements.txt`
3. Запустіть програму: `python main.py`

#### Портативна Версія
1. Завантажте портативний ZIP з релізів
2. Розпакуйте в бажане місце
3. Запустіть `WDock.exe`

#### Інсталятор Windows
1. Завантажте інсталятор з релізів
2. Запустіть файл установки
3. Слідуйте майстру встановлення

### Використання

1. **Додавання Іконок**: Перетягніть .exe файли або .lnk ярлики на док
2. **Створення Груп**: Перетягніть одну іконку на іншу для створення групи
3. **Позиціонування**: Правий клік на док → "Прикріпити до" → Оберіть край
4. **Налаштування**: Правий клік → "Налаштування" для повної конфігурації
5. **Автоприховування**: Увімкніть в налаштуваннях для автоматичного приховування

### Системні Вимоги

- Windows 10/11 (64-біт)
- Мінімум 4ГБ ОЗП
- 50МБ вільного місця на диску
- .NET Framework 4.7.2 або вищий

### Збірка з Вихідного Коду

```bash
# Встановіть залежності для збірки
pip install pyinstaller

# Зберіть виконуваний файл та інсталятор
python build.py
```

### Структура Проекту

```
WDock/
├── main.py                    # Точка входу програми
├── build.py                   # Скрипт збірки для дистрибуції
├── requirements.txt           # Залежності Python
├── src/                      # Вихідний код
│   ├── core/                # Основна логіка програми
│   │   ├── config_manager.py    # Управління конфігурацією
│   │   ├── dock_window.py       # Головне вікно доку
│   │   └── system_tray.py       # Інтеграція системного трею
│   ├── ui/                  # Компоненти користувацького інтерфейсу
│   │   ├── icon_widget.py       # Віджети іконок
│   │   ├── group_widget.py      # Віджети груп
│   │   ├── settings_window.py   # Діалог налаштувань
│   │   └── about_window.py      # Діалог "Про програму"
│   └── utils/               # Допоміжні модулі
│       ├── drag_drop.py         # Функціональність перетягування
│       ├── startup_manager.py   # Інтеграція автозапуску Windows
│       ├── performance.py       # Моніторинг продуктивності
│       └── multi_monitor.py     # Підтримка кількох моніторів
├── tests/                    # Юніт-тести
├── assets/                   # Іконки та зображення
└── docs/                     # Документація
```

### Участь у Розробці

1. Зробіть форк репозиторію
2. Створіть гілку функціональності
3. Внесіть свої зміни
4. Додайте тести для нової функціональності
5. Відправте pull request

### Ліцензія

© WDock Project. Всі права захищені.