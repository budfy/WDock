# WDock Documentation | Документація WDock

[English](#english-documentation) | [Українська](#українська-документація)

---

## English Documentation

### Table of Contents
1. [Getting Started](#getting-started)
2. [Features Overview](#features-overview)
3. [Installation Guide](#installation-guide)
4. [User Manual](#user-manual)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)
7. [Development](#development)

### Getting Started

WDock is a modern dock application for Windows that provides quick access to your favorite applications with advanced features like grouping, auto-hide, and multi-monitor support.

#### Quick Start
1. Download WDock from the releases page
2. Run the installer or extract the portable version
3. Launch WDock
4. Drag your favorite applications to the dock
5. Right-click to access settings and customization options

### Features Overview

#### Core Features
- **Adaptive Icons**: Automatically extracts and displays application icons
- **Drag & Drop**: Add applications by dragging .exe or .lnk files
- **Smart Grouping**: Drag icons together to create organized groups
- **Flexible Positioning**: Place dock on any screen edge
- **Auto-Hide**: Automatically hide when not needed

#### Advanced Features
- **Multi-Monitor Support**: Works seamlessly across multiple displays
- **DPI Scaling**: Automatically adapts to different screen resolutions
- **Theme Support**: Dark/light themes that sync with Windows
- **Performance Optimized**: Uses less than 50MB of memory
- **System Integration**: System tray, startup options, registry integration

### Installation Guide

#### System Requirements
- Windows 10 or Windows 11 (64-bit)
- 4GB RAM minimum
- 50MB free disk space
- .NET Framework 4.7.2 or higher

#### Installation Methods

##### Windows Installer (Recommended)
1. Download `WDock-1.0.0-Setup.exe` from releases
2. Run the installer as administrator
3. Follow the installation wizard
4. Choose startup options during installation
5. Launch WDock from Start Menu or Desktop

##### Portable Version
1. Download `WDock-1.0.0-Portable.zip`
2. Extract to your preferred location
3. Run `WDock.exe`
4. No installation required

##### From Source
```bash
# Clone repository
git clone https://github.com/wdock/wdock.git
cd wdock

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### User Manual

#### Adding Applications
1. **Drag & Drop**: Drag .exe files or .lnk shortcuts onto the dock
2. **Context Menu**: Right-click dock → "Add Application" (future feature)

#### Creating Groups
1. Drag one application icon onto another
2. Enter a group name when prompted
3. Choose a group icon (emoji or custom image)
4. Click on group to expand and see all applications

#### Positioning the Dock
1. Right-click on empty space in dock
2. Select "Attach to" from context menu
3. Choose desired edge: Top, Bottom, Left, or Right
4. Dock will automatically reposition

#### Customizing Appearance
1. Right-click dock → "Settings"
2. Go to "Appearance" tab
3. Adjust:
   - Icon size (32-64px)
   - Animation speed
   - Theme selection
   - Transparency

#### Auto-Hide Configuration
1. Open Settings → "Behavior" tab
2. Enable "Auto-hide"
3. Configure "Intelligent hide" for fullscreen apps
4. Set hide delay (100-5000ms)

### Configuration

#### Configuration File Location
`%APPDATA%\WDock\config.json`

#### Configuration Structure
```json
{
  "position": "bottom",
  "alignment": "center",
  "auto_hide": true,
  "intelligent_hide": true,
  "always_on_top": true,
  "theme": "auto",
  "icon_size": 48,
  "animation_speed": 200,
  "icons": [
    {
      "path": "C:\\Path\\To\\Application.exe",
      "name": "Application Name",
      "group": null
    }
  ],
  "groups": {
    "GroupName": {
      "name": "Display Name",
      "icon": "🎮",
      "items": ["path1", "path2"]
    }
  }
}
```

#### Backup and Restore
- **Export**: Settings → Advanced → "Export Settings"
- **Import**: Settings → Advanced → "Import Settings"

### Troubleshooting

#### Common Issues

##### WDock Won't Start
1. Check if Python is installed (for source version)
2. Verify all dependencies are installed
3. Run as administrator
4. Check Windows Event Viewer for errors

##### Icons Not Loading
1. Verify application paths are correct
2. Check file permissions
3. Try removing and re-adding the application
4. Restart WDock

##### Performance Issues
1. Check memory usage in Task Manager
2. Reduce number of icons
3. Disable animations in settings
4. Clear icon cache: Settings → Advanced → Clear Cache

##### Auto-Hide Not Working
1. Check auto-hide settings
2. Verify cursor is moving away from dock
3. Disable other dock applications
4. Restart WDock

#### Error Codes
- **E001**: Configuration file corrupted
- **E002**: Insufficient permissions
- **E003**: Missing dependencies
- **E004**: System compatibility issue

### Development

#### Building from Source
```bash
# Install build dependencies
pip install pyinstaller

# Build executable
python build.py

# Run tests
python tests/test_wdock.py
```

#### Project Structure
See README.md for detailed project structure.

#### Contributing
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit pull request

---

## Українська Документація

### Зміст
1. [Початок Роботи](#початок-роботи)
2. [Огляд Можливостей](#огляд-можливостей)
3. [Посібник з Встановлення](#посібник-з-встановлення)
4. [Керівництво Користувача](#керівництво-користувача)
5. [Налаштування](#налаштування)
6. [Усунення Неполадок](#усунення-неполадок)
7. [Розробка](#розробка)

### Початок Роботи

WDock - це сучасний додаток док-панелі для Windows, який забезпечує швидкий доступ до ваших улюблених програм з розширеними функціями, такими як групування, автоприховування та підтримка кількох моніторів.

#### Швидкий Старт
1. Завантажте WDock зі сторінки релізів
2. Запустіть інсталятор або розпакуйте портативну версію
3. Запустіть WDock
4. Перетягніть ваші улюблені програми на док
5. Клацніть правою кнопкою для доступу до налаштувань

### Огляд Можливостей

#### Основні Функції
- **Адаптивні Іконки**: Автоматично витягує та відображає іконки програм
- **Перетягування**: Додавайте програми перетягуванням .exe або .lnk файлів
- **Розумне Групування**: Перетягніть іконки разом для створення організованих груп
- **Гнучке Позиціонування**: Розмістіть док на будь-якому краю екрана
- **Автоприховування**: Автоматично ховається, коли не потрібен

#### Розширені Функції
- **Підтримка Кількох Моніторів**: Бездоганно працює на кількох дисплеях
- **Масштабування DPI**: Автоматично адаптується до різних роздільностей екрана
- **Підтримка Тем**: Темні/світлі теми, що синхронізуються з Windows
- **Оптимізована Продуктивність**: Використовує менше 50МБ пам'яті
- **Системна Інтеграція**: Системний трей, опції автозапуску, інтеграція з реєстром

### Посібник з Встановлення

#### Системні Вимоги
- Windows 10 або Windows 11 (64-біт)
- Мінімум 4ГБ ОЗП
- 50МБ вільного місця на диску
- .NET Framework 4.7.2 або вищий

#### Методи Встановлення

##### Інсталятор Windows (Рекомендується)
1. Завантажте `WDock-1.0.0-Setup.exe` з релізів
2. Запустіть інсталятор як адміністратор
3. Слідуйте майстру встановлення
4. Оберіть опції автозапуску під час встановлення
5. Запустіть WDock з Меню Пуск або Робочого столу

##### Портативна Версія
1. Завантажте `WDock-1.0.0-Portable.zip`
2. Розпакуйте у бажане місце
3. Запустіть `WDock.exe`
4. Встановлення не потрібне

##### З Вихідного Коду
```bash
# Клонувати репозиторій
git clone https://github.com/wdock/wdock.git
cd wdock

# Встановити залежності
pip install -r requirements.txt

# Запустити програму
python main.py
```

### Керівництво Користувача

#### Додавання Програм
1. **Перетягування**: Перетягніть .exe файли або .lnk ярлики на док
2. **Контекстне Меню**: Правий клік на док → "Додати Програму" (майбутня функція)

#### Створення Груп
1. Перетягніть одну іконку програми на іншу
2. Введіть назву групи при запиті
3. Оберіть іконку групи (емодзі або власне зображення)
4. Клацніть на групу для розгортання та перегляду всіх програм

#### Позиціонування Доку
1. Правий клік на порожньому місці доку
2. Оберіть "Прикріпити до" з контекстного меню
3. Оберіть бажаний край: Верх, Низ, Ліво або Право
4. Док автоматично перепозиціонується

#### Налаштування Зовнішнього Вигляду
1. Правий клік на док → "Налаштування"
2. Перейдіть на вкладку "Зовнішній вигляд"
3. Налаштуйте:
   - Розмір іконок (32-64px)
   - Швидкість анімації
   - Вибір теми
   - Прозорість

#### Налаштування Автоприховування
1. Відкрийте Налаштування → вкладка "Поведінка"
2. Увімкніть "Автоприховування"
3. Налаштуйте "Розумне приховування" для повноекранних програм
4. Встановіть затримку приховування (100-5000мс)

### Налаштування

#### Розташування Файлу Конфігурації
`%APPDATA%\WDock\config.json`

#### Структура Конфігурації
```json
{
  "position": "bottom",
  "alignment": "center",
  "auto_hide": true,
  "intelligent_hide": true,
  "always_on_top": true,
  "theme": "auto",
  "icon_size": 48,
  "animation_speed": 200,
  "icons": [
    {
      "path": "C:\\Шлях\\До\\Програми.exe",
      "name": "Назва Програми",
      "group": null
    }
  ],
  "groups": {
    "НазваГрупи": {
      "name": "Відображувана Назва",
      "icon": "🎮",
      "items": ["шлях1", "шлях2"]
    }
  }
}
```

#### Резервне Копіювання та Відновлення
- **Експорт**: Налаштування → Додатково → "Експорт Налаштувань"
- **Імпорт**: Налаштування → Додатково → "Імпорт Налаштувань"

### Усунення Неполадок

#### Поширені Проблеми

##### WDock Не Запускається
1. Перевірте, чи встановлений Python (для версії з вихідним кодом)
2. Переконайтеся, що всі залежності встановлені
3. Запустіть як адміністратор
4. Перевірте Переглядач подій Windows на помилки

##### Іконки Не Завантажуються
1. Переконайтеся, що шляхи до програм правильні
2. Перевірте дозволи файлів
3. Спробуйте видалити та повторно додати програму
4. Перезапустіть WDock

##### Проблеми з Продуктивністю
1. Перевірте використання пам'яті в Диспетчері завдань
2. Зменшіть кількість іконок
3. Вимкніть анімації в налаштуваннях
4. Очистіть кеш іконок: Налаштування → Додатково → Очистити Кеш

##### Автоприховування Не Працює
1. Перевірте налаштування автоприховування
2. Переконайтеся, що курсор відходить від доку
3. Вимкніть інші док-програми
4. Перезапустіть WDock

#### Коди Помилок
- **E001**: Файл конфігурації пошкоджений
- **E002**: Недостатньо дозволів
- **E003**: Відсутні залежності
- **E004**: Проблема сумісності системи

### Розробка

#### Збірка з Вихідного Коду
```bash
# Встановити залежності для збірки
pip install pyinstaller

# Зібрати виконуваний файл
python build.py

# Запустити тести
python tests/test_wdock.py
```

#### Структура Проекту
Дивіться README.md для детальної структури проекту.

#### Участь у Розробці
1. Зробіть форк репозиторію
2. Створіть гілку функціональності
3. Реалізуйте зміни з тестами
4. Відправте pull request