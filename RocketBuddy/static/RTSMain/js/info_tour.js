//document.addEventListener("DOMContentLoaded", function() {
//    const registrationButton = document.querySelector('[data-series="Daily"]');
//    const detailsButton = document.querySelector('[data-series="Weekly"]');
//    const registrationBlock = document.getElementById('1');
//    const detailsBlock = document.getElementById('2');
//
//    detailsBlock.style.display = 'none';
//
//    playerInfoCheckboxes.forEach(function(mainCheckbox) {
//        const reserveCheckbox = mainCheckbox.closest('.col-sm-3').nextElementSibling.querySelector('input[name="reserve_cast"]');
//
//        mainCheckbox.addEventListener('change', function() {
//            if (this.checked) {
//                reserveCheckbox.checked = false; // Снимаем галочку с резервного чекбокса
//            }
//        });
//
//        reserveCheckbox.addEventListener('change', function() {
//            if (this.checked) {
//                mainCheckbox.checked = false; // Снимаем галочку с основного чекбокса
//            }
//        });
//    });
//
//    detailsButton.addEventListener('click', function() {
//        // Перемещаем блок с деталями турнира перед блоком с выбором команды
//        registrationBlock.parentNode.insertBefore(detailsBlock, registrationBlock);
//        // Скрываем блок с выбором команды
//        registrationBlock.style.display = 'none';
//        // Показываем блок с деталями турнира
//        detailsBlock.style.display = 'block';
//    });
//
//    registrationButton.addEventListener('click', function() {
//        // Перемещаем блок с выбором команды перед блоком с деталями турнира
//        detailsBlock.parentNode.insertBefore(registrationBlock, detailsBlock);
//        // Скрываем блок с деталями турнира
//        detailsBlock.style.display = 'none';
//        // Показываем блок с выбором команды
//        registrationBlock.style.display = 'block';
//    });
//});