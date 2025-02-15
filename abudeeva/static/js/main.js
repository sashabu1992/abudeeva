let csrfToken;  // Глобальная переменная для CSRF-токена

// Функция для склонения слова "товар"
function pluralizeProducts(count) {
    if (count % 10 === 1 && count % 100 !== 11) {
        return `${count} товар`;
    } else if (count % 10 >= 2 && count % 10 <= 4 && (count % 100 < 10 || count % 100 >= 20)) {
        return `${count} товара`;
    } else {
        return `${count} товаров`;
    }
}

// Функция для форматирования цены
function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'decimal',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(price);
}

// Функция для обновления количества товаров
function updateCartCount(count) {
    const cartCountTextElements = document.querySelectorAll('.cart-count-text');
    cartCountTextElements.forEach(element => {
        element.textContent = pluralizeProducts(count);
    });

    const cartCountNumberElements = document.querySelectorAll('.cart-count-number');
    cartCountNumberElements.forEach(element => {
        element.textContent = count;
    });
}

// Функция для обновления цены
function updateCartPrice(totalPrice) {
    const formattedPrice = formatPrice(totalPrice);
    const totalPriceElements = document.querySelectorAll('.total-price');
    totalPriceElements.forEach(element => {
        element.textContent = formattedPrice;
    });
}

// Инициализация CSRF-токена
document.addEventListener('DOMContentLoaded', function() {
    csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
});

// Обработчик для добавления товара в корзину
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form.add-to-cart-form');

    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(form);
            const url = form.getAttribute('action');

            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    swal("Поздравляем!", "Товар успешно добавлен в корзину!", "success");
                    updateCartCount(data.cart_count);  // Обновляем количество товаров
                    updateCartPrice(data.total_price); // Обновляем общую стоимость
                } else {
                    alert('Ошибка при добавлении товара в корзину: ' + data.error);
                    swal("Внимание!", "Ошибка при добавлении товара в корзину", "error");
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
               swal("Внимание!", "Ошибка при добавлении товара в корзину", "error");
            });
        });
    });
});

// Обработчик для удаления товара из корзины
document.addEventListener('DOMContentLoaded', function() {
    const removeButtons = document.querySelectorAll('.remove-from-cart-btn');

    removeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            const key = button.getAttribute('data-key');
            const url = `/shop/remove_from_cart/${key}/`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    swal("Внимание!", "Товар успешно удален из корзины!", "info");

                    // Удаляем элемент из DOM
                    const cartItem = document.querySelector(`.cart-item[data-key="${key}"]`);
                    if (cartItem) {
                        cartItem.remove();
                    }

                    updateCartPrice(data.total_price); // Обновляем общую стоимость
                    updateCartCount(data.cart_count);  // Обновляем количество товаров

                    // Если корзина пуста, показываем сообщение
                    if (data.cart_count === 0) {
                        const cartItemsContainer = document.querySelector('.cart-items');
                        if (cartItemsContainer) {
                            cartItemsContainer.innerHTML = '<p>Ваша корзина пуста.</p>';
                        }
                    }
                } else {
                    swal("Внимание!", "Ошибка при удалении товара из корзины", "error");
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
               swal("Внимание!", "Ошибка при удалении товара из корзины", "error");
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const quantityControls = document.querySelectorAll('.quantity-control');

    quantityControls.forEach(control => {
        const decreaseButton = control.querySelector('.quantity-decrease');
        const increaseButton = control.querySelector('.quantity-increase');
        const quantityValue = control.querySelector('.quantity-value');
        const key = decreaseButton.getAttribute('data-key');

        decreaseButton.addEventListener('click', function() {
            updateQuantity(key, -1, control);
        });

        increaseButton.addEventListener('click', function() {
            updateQuantity(key, 1, control);
        });
    });

    function updateQuantity(key, delta, control) {
        const url = `/shop/update_cart_quantity/${key}/`;
        const currentQuantity = parseInt(control.querySelector('.quantity-value').textContent, 10);
        const newQuantity = currentQuantity + delta;

        if (newQuantity < 1) {
            swal("Внимание!", "Количество не может быть меньше 1", "info");
            return;
        }

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity: newQuantity }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Обновляем значение в текущей строке (кнопки "+" и "-")
                control.querySelector('.quantity-value').textContent = newQuantity;

                // Обновляем количество товара в строке (текст "кол-во: X")
                const cartItem = control.closest('.cart-item');
                if (cartItem) {
                    const quantitySpan = cartItem.querySelector('.property span.item-quantity');
                    if (quantitySpan) {
                        quantitySpan.textContent = newQuantity;
                    }
                }

                // Обновляем общую стоимость
                updateCartPrice(data.total_price);

                // Обновляем количество товаров в корзине
                updateCartCount(data.cart_count);
            } else {
                swal("Внимание!", "Ошибка при обновлении количества товара", "error");
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            swal("Внимание!", "Ошибка при обновлении количества товара", "error");
        });
    }


});


  //отправка корзины
  document.addEventListener('DOMContentLoaded', function() {
    // Находим кнопку "Оформить заказ"
    const cartSendButton = document.getElementById('cart-send');

    // Находим форму
    const orderForm = document.getElementById('order-form');

    // Добавляем обработчик события на кнопку
    cartSendButton.addEventListener('click', function() {
        // Вызываем метод submit() у формы
        orderForm.dispatchEvent(new Event('submit'));
    });

    // Обработчик отправки формы
    orderForm.addEventListener('submit', function(e) {
        e.preventDefault();  // Предотвращаем стандартную отправку формы

        const form = e.target;
        const formData = new FormData(form);

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'),  // Добавляем CSRF-токен
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Перенаправляем на страницу благодарности
                window.location.href = data.redirect_url;
            } else {
                // Показываем ошибки, если они есть
                alert('Ошибка: ' + JSON.stringify(data.errors));
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
    });
});

  // работа с опцией цвета
   document.addEventListener('DOMContentLoaded', function() {
        // Находим все радио-кнопки и блок с текстом
        const radioButtons = document.querySelectorAll('input[name="color"]');
        const colorNameSpan = document.querySelector('.colors_name');

        // Функция для обновления текста и добавления класса active
        function updateSelectedColor() {
            // Убираем класс active у всех элементов
            document.querySelectorAll('.obv').forEach(obv => {
                obv.classList.remove('active');
            });

            // Находим выбранную радио-кнопку
            const selectedRadio = document.querySelector('input[name="color"]:checked');

            // Если есть выбранная радио-кнопка
            if (selectedRadio) {
                // Добавляем класс active к выбранному элементу
                selectedRadio.closest('label').querySelector('.obv').classList.add('active');

                // Обновляем текст в .colors_name
                const selectedColorName = selectedRadio.getAttribute('data-name');
                colorNameSpan.textContent = selectedColorName;
            }
        }

        // Вызываем функцию при загрузке страницы
        updateSelectedColor();

        // Добавляем обработчик события для каждой радио-кнопки
        radioButtons.forEach(radio => {
            radio.addEventListener('change', updateSelectedColor);
        });
    });

   //кнопка favorite
 document.addEventListener('DOMContentLoaded', function() {
        // Находим кнопку
        const favorButton = document.querySelector('.btn-favor');

        // Добавляем обработчик события на клик по кнопке
        if (favorButton) {
            favorButton.addEventListener('click', function(event) {
                event.preventDefault(); // Предотвращаем стандартное поведение кнопки

                // Показываем сообщение "В разработке"
                swal("Внимание!", "Функция Добавить в избранное в разработке", "info");
            });
        }
    });

 // tabs
  document.addEventListener('DOMContentLoaded', function() {
        const accordionItems = document.querySelectorAll('.accordion-item');

        accordionItems.forEach(item => {
            const header = item.querySelector('.accordion-header');

            header.addEventListener('click', () => {
                // Закрываем все открытые элементы
                accordionItems.forEach(otherItem => {
                    if (otherItem !== item && otherItem.classList.contains('active')) {
                        otherItem.classList.remove('active');
                    }
                });

                // Открываем/закрываем текущий элемент
                item.classList.toggle('active');
            });
        });
    });