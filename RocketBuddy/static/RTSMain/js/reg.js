function copyToClipboard() {
    var teamLink = document.getElementById("team-link");
    var linkText = teamLink.textContent || teamLink.innerText;

    navigator.clipboard.writeText(linkText)
        .then(function () {
            alert("Ссылка скопирована в буфер обмена: " + linkText);
        })
        .catch(function () {
            alert("Ошибка при копировании ссылки");
        });
}


//document.addEventListener('DOMContentLoaded', function() {
//            // Получаем ссылки на кнопки и таблицы
//            var btnTable1 = document.getElementById('btn-table1');
//            var btnTable2 = document.getElementById('btn-table2');
//            var table1 = document.getElementById('table1');
//            var table2 = document.getElementById('table2');
//
//            // Обработчик для кнопки "Таблица 1"
//            btnTable1.addEventListener('click', function() {
//                table1.style.display = 'block';
//                table2.style.display = 'none';
//            });
//
//            // Обработчик для кнопки "Таблица 2"
//            btnTable2.addEventListener('click', function() {
//                table1.style.display = 'none';
//                table2.style.display = 'block';
//            });
//        });


// Функция для выполнения поиска
//      function searchTable() {
//        // Получаем введенный пользователем запрос
//        var input, filter, table, tr, td, i, j, txtValue;
//        input = document.getElementById("search_input"); // Здесь "search_input" - это ID вашего поля для ввода поискового запроса
//        filter = input.value.toUpperCase();
//        table = document.getElementById("table1");
//        table2 = document.getElementById("table2");// Здесь "table1" - это ID вашей таблицы
//        tbody = table.getElementsByTagName("tbody")[0]
//        tbody2 = table2.getElementsByTagName("tbody")[0]
//        tr = tbody.getElementsByTagName("tr");
//        tr2 = tbody2.getElementsByTagName("tr");
//
//
//        // Проходим по всем строкам таблицы
//        for (i = 0; i < tr.length; i++) {
//          tds = tr[i].getElementsByTagName("td");
//          match = false;
//
//          // Проходим по всем ячейкам в строке
//          for (j = 0; j < tds.length; j++) {
//            td = tds[j];
//            if (td) {
//              txtValue = td.textContent || td.innerText;
//              if (txtValue.toUpperCase().indexOf(filter) > -1) {
//                match = true;
//                break; // Если совпадение найдено, выходим из цикла
//              }
//            }
//          }
//
//          // Отображаем или скрываем строку в зависимости от результата поиска
//          if (match) {
//            tr[i].style.display = "";
//          } else {
//            tr[i].style.display = "none";
//          }
//        }
//
//
//
//
//        for (i = 0; i < tr2.length; i++) {
//          tds = tr2[i].getElementsByTagName("td");
//          match = false;
//
//          // Проходим по всем ячейкам в строке
//          for (j = 0; j < tds.length; j++) {
//            td2 = tds[j];
//            if (td) {
//              txtValue = td2.textContent || td2.innerText;
//              if (txtValue.toUpperCase().indexOf(filter) > -1) {
//                match = true;
//                break; // Если совпадение найдено, выходим из цикла
//              }
//            }
//          }
//
//          // Отображаем или скрываем строку в зависимости от результата поиска
//          if (match) {
//            tr2[i].style.display = "";
//          } else {
//            tr2[i].style.display = "none";
//          }
//        }
//      }
//
//      // Навешиваем обработчик события на поле ввода
//      var searchInput = document.getElementById("search_input");
//      if (searchInput) {
//        searchInput.addEventListener("keyup", searchTable);
//      }


// Функция для выполнения поиска
function searchTableUsers() {
    // Получаем введенный пользователем запрос
    var input, filter, table, tr, td, i, j, txtValue;
    input = document.getElementById("search_input_users"); // Здесь "search_input" - это ID вашего поля для ввода поискового запроса
    filter = input.value.toUpperCase();
    table = document.getElementById("table_users");
    tbody = table.getElementsByTagName("tbody")[0]
    tr = tbody.getElementsByTagName("tr");


    // Проходим по всем строкам таблицы
    for (i = 0; i < tr.length; i++) {
        tds = tr[i].getElementsByTagName("td");
        match = false;

        // Проходим по всем ячейкам в строке
        for (j = 0; j < tds.length; j++) {
            td = tds[j];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    match = true;
                    break; // Если совпадение найдено, выходим из цикла
                }
            }
        }

        // Отображаем или скрываем строку в зависимости от результата поиска
        if (match) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
    }

}

// Навешиваем обработчик события на поле ввода
var searchInput = document.getElementById("search_input");
if (searchInput) {
    searchInput.addEventListener("keyup", searchTable);
}


document.addEventListener("DOMContentLoaded", function () {
    const playerInfoCheckboxes = document.querySelectorAll('input[name="player_info"]');
    const reserveCastCheckboxes = document.querySelectorAll('input[name="reserve_cast"]');

    playerInfoCheckboxes.forEach(function (mainCheckbox) {
        const reserveCheckbox = mainCheckbox.closest('.col-xl-6').querySelector('input[name="reserve_cast"]');

        mainCheckbox.addEventListener('change', function () {
            if (this.checked) {
                reserveCheckbox.checked = false; // Снимаем галочку с резервного чекбокса
            }
        });

        reserveCheckbox.addEventListener('change', function () {
            if (this.checked) {
                mainCheckbox.checked = false; // Снимаем галочку с основного чекбокса
            }
        });
    });

    // Проверяем существование кнопок и блоков
    const registrationButton = document.querySelector('[data-series="Register"]');
    const detailsButton = document.querySelector('[data-series="Detail"]');
    const bracketButton = document.querySelector('[data-series="Bracket"]');
    const regulationButton = document.querySelector('[data-series="Regulation"]');
    const chatButton = document.querySelector('[data-series="Chat"]'); // Добавлена кнопка чата

    const registrationBlock = document.getElementById('1');
    const detailsBlock = document.getElementById('2');
    const bracketBlock = document.getElementById('3');
    const regulationBlock = document.getElementById('4');
    const chatBlock = document.getElementById('5'); // Добавлен блок чата

    if (registrationButton && detailsButton && bracketButton && regulationButton && chatButton) {
        registrationBlock.style.display = 'none';
        bracketBlock.style.display = 'none';
        regulationBlock.style.display = 'none';
        chatBlock.style.display = 'none';

        detailsButton.addEventListener('click', function () {
            detailsBlock.parentNode.insertBefore(detailsBlock, bracketBlock);
            registrationBlock.style.display = 'none';
            bracketBlock.style.display = 'none';
            regulationBlock.style.display = 'none';
            chatBlock.style.display = 'none'; // Скрываем блок чата
            detailsBlock.style.display = 'block';
        });

        registrationButton.addEventListener('click', function () {
            registrationBlock.parentNode.insertBefore(registrationBlock, detailsBlock);
            detailsBlock.style.display = 'none';
            bracketBlock.style.display = 'none';
            regulationBlock.style.display = 'none';
            chatBlock.style.display = 'none'; // Скрываем блок чата
            registrationBlock.style.display = 'block';
        });

        bracketButton.addEventListener('click', function () {
            bracketBlock.parentNode.insertBefore(bracketBlock, registrationBlock);
            detailsBlock.style.display = 'none';
            registrationBlock.style.display = 'none';
            regulationBlock.style.display = 'none';
            chatBlock.style.display = 'none'; // Скрываем блок чата
            bracketBlock.style.display = 'block';
        });

        regulationButton.addEventListener('click', function () {
            regulationBlock.parentNode.insertBefore(regulationBlock, bracketBlock);
            bracketBlock.style.display = 'none';
            registrationBlock.style.display = 'none';
            detailsBlock.style.display = 'none';
            chatBlock.style.display = 'none'; // Скрываем блок чата
            regulationBlock.style.display = 'block';
        });

        chatButton.addEventListener('click', function () { // Новый обработчик для кнопки чата
            chatBlock.parentNode.insertBefore(chatBlock, regulationBlock);
            bracketBlock.style.display = 'none';
            registrationBlock.style.display = 'none';
            detailsBlock.style.display = 'none';
            regulationBlock.style.display = 'none';
            chatBlock.style.display = 'block'; // Показываем блок чата
        });
    }


    const settingListButton = document.querySelector('[data-series="Setting"]');
    const applicationsListButton = document.querySelector('[data-series="Applications"]');
    const groupsListButton = document.querySelector('[data-series="Groups"]');
    const infoTourListButton = document.querySelector('[data-series="InfoTour"]');

    const settingBlock = document.getElementById('setting');
    const applicationsBlock = document.getElementById('applications_list');
    const groupsBlock = document.getElementById('groups_list');
    const infoTourBlock = document.getElementById('info_tour_list');

    if (settingListButton && applicationsListButton && groupsListButton && infoTourListButton && applicationsBlock && settingBlock && groupsBlock && infoTourBlock) {
        // Скрываем все блоки по умолчанию
        applicationsBlock.style.display = 'none';
        groupsBlock.style.display = 'none';
        infoTourBlock.style.display = 'none';

        // Обработчик для кнопки "Настройки"
        settingListButton.addEventListener('click', function () {
            applicationsBlock.style.display = 'none';
            groupsBlock.style.display = 'none';
            infoTourBlock.style.display = 'none';
            settingBlock.style.display = 'block';
        });

        // Обработчик для кнопки "Заявки"
        applicationsListButton.addEventListener('click', function () {
            settingBlock.style.display = 'none';
            groupsBlock.style.display = 'none';
            infoTourBlock.style.display = 'none';
            applicationsBlock.style.display = 'block';
        });

        // Обработчик для кнопки "Группы"
        groupsListButton.addEventListener('click', function () {
            settingBlock.style.display = 'none';
            applicationsBlock.style.display = 'none';
            infoTourBlock.style.display = 'none';
            groupsBlock.style.display = 'block';
        });

        // Обработчик для кнопки "Информация о турнире"
        infoTourListButton.addEventListener('click', function () {
            settingBlock.style.display = 'none';
            applicationsBlock.style.display = 'none';
            groupsBlock.style.display = 'none';
            infoTourBlock.style.display = 'block';
        });
    }


});



