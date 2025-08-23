# Git Flow Setup | Налаштування Git Flow

## English

### Repository Setup Complete

The WDock project has been successfully connected to the remote repository and git flow has been enabled.

#### Repository Details
- **Remote Repository**: https://github.com/budfy/WDock.git
- **Main Branch**: `main` (production-ready code)
- **Development Branch**: `develop` (integration branch for features)

#### Git Flow Configuration
Git flow has been initialized with the following branch structure:

| Branch Type | Prefix | Purpose |
|-------------|--------|---------|
| **Production** | `main` | Stable releases |
| **Development** | `develop` | Feature integration |
| **Features** | `feature/` | New feature development |
| **Releases** | `release/` | Release preparation |
| **Hotfixes** | `hotfix/` | Critical production fixes |
| **Bugfixes** | `bugfix/` | Bug fixes for develop |
| **Support** | `support/` | Maintenance branches |

#### Initial Commit
The initial commit includes:
- ✅ Complete WDock application with PyQt6
- ✅ Dynamic theme support (light/dark/auto)
- ✅ CSS-like alignment behavior implementation
- ✅ Context menu functionality
- ✅ Settings window with theme integration
- ✅ System tray integration
- ✅ Lucide.dev icon integration
- ✅ Multi-monitor support
- ✅ Performance monitoring
- ✅ Comprehensive test suite
- ✅ Bilingual documentation

#### Git Flow Commands
```bash
# Start a new feature
git flow feature start feature-name

# Finish a feature
git flow feature finish feature-name

# Start a release
git flow release start 1.0.0

# Finish a release
git flow release finish 1.0.0

# Start a hotfix
git flow hotfix start hotfix-name

# Finish a hotfix
git flow hotfix finish hotfix-name
```

---

## Українська

### Налаштування Репозиторію Завершено

Проєкт WDock успішно підключено до віддаленого репозиторію та увімкнено git flow.

#### Деталі Репозиторію
- **Віддалений Репозиторій**: https://github.com/budfy/WDock.git
- **Основна Гілка**: `main` (готовий до продакшену код)
- **Гілка Розробки**: `develop` (гілка інтеграції для функцій)

#### Конфігурація Git Flow
Git flow ініціалізовано з наступною структурою гілок:

| Тип Гілки | Префікс | Призначення |
|-----------|---------|-------------|
| **Продакшен** | `main` | Стабільні релізи |
| **Розробка** | `develop` | Інтеграція функцій |
| **Функції** | `feature/` | Розробка нових функцій |
| **Релізи** | `release/` | Підготовка релізів |
| **Хотфікси** | `hotfix/` | Критичні виправлення продакшену |
| **Багфікси** | `bugfix/` | Виправлення помилок для develop |
| **Підтримка** | `support/` | Гілки підтримки |

#### Початковий Комміт
Початковий комміт включає:
- ✅ Повний застосунок WDock з PyQt6
- ✅ Динамічна підтримка тем (світла/темна/авто)
- ✅ Реалізація CSS-подібного вирівнювання
- ✅ Функціональність контекстного меню
- ✅ Вікно налаштувань з інтеграцією тем
- ✅ Інтеграція системного трею
- ✅ Інтеграція іконок Lucide.dev
- ✅ Підтримка декількох моніторів
- ✅ Моніторинг продуктивності
- ✅ Комплексний набір тестів
- ✅ Двомовна документація

#### Команди Git Flow
```bash
# Початок нової функції
git flow feature start назва-функції

# Завершення функції
git flow feature finish назва-функції

# Початок релізу
git flow release start 1.0.0

# Завершення релізу
git flow release finish 1.0.0

# Початок хотфіксу
git flow hotfix start назва-хотфіксу

# Завершення хотфіксу
git flow hotfix finish назва-хотфіксу
```

### Development Workflow | Робочий Процес Розробки

#### Feature Development | Розробка Функцій
1. Start from `develop` branch | Почати з гілки `develop`
2. Create feature branch | Створити гілку функції
3. Develop and test | Розробити та протестувати
4. Merge back to `develop` | Злити назад в `develop`

#### Release Process | Процес Релізу
1. Create release branch from `develop` | Створити гілку релізу з `develop`
2. Final testing and bug fixes | Фінальне тестування та виправлення
3. Merge to `main` and tag | Злити в `main` та створити тег
4. Merge back to `develop` | Злити назад в `develop`

#### Hotfix Process | Процес Хотфіксу
1. Create hotfix branch from `main` | Створити гілку хотфіксу з `main`
2. Fix critical issue | Виправити критичну проблему
3. Merge to both `main` and `develop` | Злити в `main` та `develop`