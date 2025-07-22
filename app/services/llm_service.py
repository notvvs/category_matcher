import httpx
import logging
from typing import Optional

from app.core.settings import settings

logger = logging.getLogger(__name__)


class OllamaCategorizer:
    def __init__(self):
        self.model_name = settings.MODEL_NAME
        self.llm_url = settings.LLM_URL

    def categorize_product(self, product_name: str, description: str, category_list: list) -> Optional[str]:
        """Категоризирует товар используя Ollama"""

        prompt = f"""
Ты - эксперт по категоризации товаров. Твоя задача - присвоить товару наиболее подходящую категорию из предоставленного списка.

### Входные данные:
- **Название товара:** [название]
- **Описание товара:** [описание]
- **Доступные категории:** [список категорий]

### Правила категоризации:
1. Выбирай категорию ТОЛЬКО из предоставленного списка
2. Анализируй все данные о товаре: название, описание, характеристики
3. Если товар может подходить к нескольким категориям, выбирай наиболее специфичную
4. При сомнениях выбирай категорию, к которой товар относится в первую очередь
5. Учитывай контекст использования товара

### Формат ответа:
Отвечай ТОЛЬКО названием категории без дополнительных слов, объяснений или форматирования.

### Пример:
**Товар:** Apple iPhone 15 Pro
**Описание:** Смартфон с экраном 6.1", камерой 48МП, процессором A17 Pro
**Категории:** [Электроника, Смартфоны, Аксессуары, Компьютеры]

**Ответ:**
Смартфоны

---

## Шаблон для использования:

**Товар:** {product_name}
**Описание:** {description}
**Доступные категории:** {category_list}

Определи наиболее подходящую категорию согласно инструкции выше."""

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "top_k": 10
            }
        }

        try:
            response = httpx.post(
                f"{self.llm_url.rstrip('/')}/api/generate",
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            result = response.json()
            raw_answer = result.get('response', '').strip()

            if not raw_answer:
                logger.warning("Empty response from LLM service")
                return None

            return raw_answer

        except httpx.TimeoutException:
            logger.error("LLM service timeout")
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"LLM service HTTP error: {e.response.status_code}")
            return None
        except httpx.RequestError as e:
            logger.error(f"LLM service connection error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in LLM service: {e}")
            return None