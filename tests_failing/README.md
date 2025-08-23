# Failing Tests | Невдалі Тести

## English

This directory contains tests that are currently failing and need to be fixed.

### Failed Tests Overview

#### `test_basic.py`
**Status**: ❌ Failing  
**Issue**: Assertion error in configuration test  
**Error**: `assert config.get("position") == "bottom"` fails  
**Root Cause**: Configuration may have different default values or existing configuration file

#### `test_wdock.py` 
**Status**: ❌ Multiple failures and errors  
**Issues**:
1. **Configuration Tests**: Tests expect clean state but configuration may persist from previous runs
2. **QPainter Mock Issue**: `create_drag_pixmap` test fails due to PyQt6 QPainter mock compatibility
3. **Icon Management**: Add/remove icon tests fail due to existing icons in configuration

### Failures Summary

| Test | Failures | Errors | Root Cause |
|------|----------|--------|------------|
| `test_basic.py` | 1 | 0 | Configuration assertion |
| `test_wdock.py` | 5 | 1 | Config persistence + PyQt6 mocking |

### Fix Recommendations

1. **Configuration Isolation**: Tests should create isolated temporary configuration files
2. **State Management**: Clear configuration state before each test
3. **PyQt6 Compatibility**: Update mocking approach for PyQt6 QPainter objects
4. **Test Independence**: Ensure tests don't depend on global application state

---

## Українська

Ця директорія містить тести, які наразі не проходять і потребують виправлення.

### Огляд Невдалих Тестів

#### `test_basic.py`
**Статус**: ❌ Не проходить  
**Проблема**: Помилка твердження в тесті конфігурації  
**Помилка**: `assert config.get("position") == "bottom"` не проходить  
**Причина**: Конфігурація може мати інші значення за замовчуванням або існуючий файл конфігурації

#### `test_wdock.py`
**Статус**: ❌ Множинні помилки  
**Проблеми**:
1. **Тести Конфігурації**: Тести очікують чистий стан, але конфігурація може зберігатися з попередніх запусків
2. **Проблема Mock QPainter**: Тест `create_drag_pixmap` не проходить через сумісність mock з PyQt6 QPainter
3. **Управління Іконками**: Тести додавання/видалення іконок не проходять через існуючі іконки в конфігурації

### Підсумок Помилок

| Тест | Помилки | Критичні помилки | Причина |
|------|---------|------------------|---------|
| `test_basic.py` | 1 | 0 | Твердження конфігурації |
| `test_wdock.py` | 5 | 1 | Збереження конфігурації + макування PyQt6 |

### Рекомендації для Виправлення

1. **Ізоляція Конфігурації**: Тести повинні створювати ізольовані тимчасові файли конфігурації
2. **Управління Станом**: Очищати стан конфігурації перед кожним тестом
3. **Сумісність з PyQt6**: Оновити підхід до макування для об'єктів QPainter PyQt6
4. **Незалежність Тестів**: Забезпечити, щоб тести не залежали від глобального стану застосунку

### Test Execution Notes | Примітки Виконання Тестів

To run failing tests:
```bash
python tests_failing/test_basic.py
python tests_failing/test_wdock.py
```

Для запуску невдалих тестів:
```bash
python tests_failing/test_basic.py
python tests_failing/test_wdock.py
```