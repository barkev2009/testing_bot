// Маршрутизация
if (udm:(not ifnull(задача))) {
    udm:(Задача:завершить_задачу(задача, '', Задача:Статус_задачи:по_коду("выполнена_исполнителем")[0]));

    // Если происходит акцепт со стороны руководителя СУР
    if (udm:(задача.тип_задачи.код ? ['согласование_правок_сур', 'согласование_правок_сур_пс'] и actionName = 'акцепт')) {
        udm:(task_type := 'согласование_правок_сур');
        var param = {
            code_subject : 'согласование_правок_сур',
            code_text : 'согласование_правок_сур',
            address: [udm:(задача.инициатор.email)],
            user_login : udm:(задача.инициатор.логин)
        }

        if (udm:(заявка.тип_заявки.код == 'транш' и не ifnull(заявка.родительская_заявка))) {
            var dogovori = udm:(Оформление_сделки:Договор:актуальные_по_заявке_и_коду_вида_договора(заявка, 'залог') || Оформление_сделки:Договор:актуальные_по_заявке_и_коду_вида_договора(заявка.родительская_заявка, 'залог')); 
        } else {
            var dogovori = udm:(Оформление_сделки:Договор:актуальные_по_заявке(заявка));
        }
        var status = udm:(Оформление_сделки:Статус_согласования_договора:актуальные_по_коду('согласование_правок')[0]);
        dogovori.forEach(function(dogovor){
            var history = udm:(Оформление_сделки:История_согласования:черновой_по_договору(js:Оформление_сделки:Договор(dogovor))[0]);
            if (!!history) {
                history.статус_согласования = status;
                dogovor.статус_согласования = status;
            }
        });
        
        udm:(Кредитная_заявка:email_cred_app(задача.заявка, js:variant(param)));
        var taskType;
        if (udm:(заявка.этап.код = 'подготовка_код')) {
            taskType = 'согласование_правок_юд';
        } else {
            taskType = 'согласование_правок_юд_пс';
        }
        udm:(Задача_заявки:создать_назначить_задачу(Политика_безопасности:Подразделение_система:по_коду('юд')[0].подразделение.руководитель, 'Согласование правок КОД по заявке', 'Правки КОД согласованы на уровне СУР, необходимо согласование ЮД', Задача:Тип_задачи:актуальные_по_коду(js:string(taskType))[0], задача.заявка, пользователь));
    // Если происходит отправка на акцепт руководителю ДР
    } else if (udm:(задача.тип_задачи.код ? ['согласование_правок_сур', 'согласование_правок_сур_пс'] и actionName = 'на_акцепт')) {
        udm:(task_type := 'согласование_правок_сур');
        udm:(user := Политика_безопасности:Подразделение_система:по_коду('сур')[0].подразделение.руководитель);
        var param = {
            code_subject : 'требуется_акцепт',
            code_text : 'требуется_акцепт',
            address: [udm:(user.email)],
            user_login : udm:(user.логин)
        }

        var history = udm:(Задача_заявки:изменить_задачу_заявки(задача, Задача:Статус_задачи:по_коду("требуется_акцепт")[0], нд(), user, '', задача.срок_исполнения, "Ожидается акцепт"));
        // присвоим задаче акцептующего
        history.дата_действия = udm:(ДАТАСЕК(js:Задача:История_задачи(history).дата_действия, 1)); 
        udm:(задача.акцептующий := user);
        udm:(Кредитная_заявка:email_cred_app(задача.заявка, js:variant(param)));
        
        // назначаем счетчик задачи на акцептующего
        udm:(Задача:назначить_счетчик(задача, user));
        // Создаем историю
        udm:(Задача_заявки:создать_историю_заявки_задача(заявка, 'Запрошен акцепт руководителя СУР', параметры.пользователь, задача.исполнитель, задача));
    // Если происходит отправка на акцепт руководителю ЮД (для подготовки КОД и подготовки к сделке одинаковы)
    } else if (udm:(задача.тип_задачи.код ? ['согласование_правок_юд', 'согласование_правок_юд_пс'] и actionName = 'на_акцепт')) {
        udm:(task_type := 'согласование_правок_юд');
        udm:(user := Политика_безопасности:Подразделение_система:по_коду('юд')[0].подразделение.руководитель);
        var param = {
            code_subject : 'требуется_акцепт',
            code_text : 'требуется_акцепт',
            address: [udm:(user.email)],
            user_login : udm:(user.логин)
        }

        var history = udm:(Задача_заявки:изменить_задачу_заявки(задача, Задача:Статус_задачи:по_коду("требуется_акцепт")[0], нд(), user, '', задача.срок_исполнения, "Ожидается акцепт"));
        // присвоим задаче акцептующего
        history.дата_действия = udm:(ДАТАСЕК(js:Задача:История_задачи(history).дата_действия, 1)); 
        udm:(задача.акцептующий := user);
        udm:(Кредитная_заявка:email_cred_app(задача.заявка, js:variant(param)));
        
        // назначаем счетчик задачи на акцептующего
        udm:(Задача:назначить_счетчик(задача, user));
        // Создаем историю
        udm:(Задача_заявки:создать_историю_заявки_задача(заявка, 'Запрошен акцепт руководителя ЮД', параметры.пользователь, задача.исполнитель, задача));
    // Если происходит акцепт со стороны руководителя ЮД (для подготовки к сделке не создаем новую задачу)
    } else if (udm:(задача.тип_задачи.код ? ['согласование_правок_юд', 'согласование_правок_юд_пс'] и actionName = 'акцепт')) {
        udm:(task_type := 'согласование_правок_юд')

        var param = {
            code_subject : 'согласование_правок_юд',
            code_text : 'согласование_правок_юд',
            address: [udm:(задача.инициатор.email)],
            user_login : udm:(задача.инициатор.логин)
        }
        udm:(Кредитная_заявка:email_cred_app(задача.заявка, js:variant(param)));

        var app = udm:(задача.заявка);
        if (udm:(не проект_решения.принятие_решения_ул)) {
            app.статус = udm:(Кредитная_заявка:Статус_заявки:по_коду('экспертизы')[0]);
            app.этап = udm:(Кредитная_заявка:Этап_рассмотрения:по_коду('экспертиза')[0]);
            var history = udm:(Кредитная_заявка:создание_истории_заявки(js:Кредитная_заявка:Кредитная_заявка(app), "По заявке требуется согласование КК, возврат на этап экспертиз", js:Кредитная_заявка:Кредитная_заявка(app).срок_рассмотрения, js:Кредитная_заявка:Кредитная_заявка(app).кредитный_аналитик, пользователь));
            history.дата_действия = udm:(ДАТАСЕК(js:Кредитная_заявка:История_заявки(history).дата_действия, 1)); //сдвигаем дату, чтобы запись была позже записи с формы (в правильном порядке)
            
            udm:(Оформление_сделки:деактуализация_сущностей_по_заявке(заявка));

            udm:(runprocess("Основной_интерфейс.Процессы.Системные.Отправка_сообщения_заявка", ["заявка"], заявка));
        } else {				
            if (udm:(заявка.тип_заявки.код == 'транш' и не ifnull(заявка.родительская_заявка))) {
                var dogovori = udm:(Оформление_сделки:Договор:актуальные_по_заявке_и_коду_вида_договора(заявка, 'залог') || Оформление_сделки:Договор:актуальные_по_заявке_и_коду_вида_договора(заявка.родительская_заявка, 'залог')); 
            } else {
                var dogovori = udm:(Оформление_сделки:Договор:актуальные_по_заявке(заявка));
            }
            var status = udm:(Оформление_сделки:Статус_согласования_договора:актуальные_по_коду('согласование_клиента')[0]);
            dogovori.forEach(function(dogovor){
                var history = udm:(Оформление_сделки:История_согласования:черновой_по_договору(js:Оформление_сделки:Договор(dogovor))[0]);
                if (!!history) {
                    history.статус_согласования = status;
                    dogovor.статус_согласования = status;
                }
            });
            if (udm:(задача.тип_задачи.код = 'согласование_правок_юд')) {
                app.статус = udm:(Кредитная_заявка:Статус_заявки:по_коду('согласование_код')[0]);
                var ispolnitel = app.менеджер_по_продажам;
                var task = udm:(Задача_заявки:создать_задачу_заявки(js:Кредитная_заявка:Кредитная_заявка(app), НД(), 'Согласование КОД с клиентом', Задача:Тип_задачи:актуальные_по_коду('согласование_код')[0], нд(), нд(), js:Политика_безопасности:Пользователь(ispolnitel)));
                udm:(Задача_заявки:создать_историю_заявки_задача(js:Кредитная_заявка:Кредитная_заявка(app), "Предварительная подготовка КОД завершена, необходимо согласование с клиентом", пользователь, js:Политика_безопасности:Пользователь(ispolnitel), js:Задача:Задача(task)));
                var history = udm:(Задача:назначить_задачу(js:Задача:Задача(task), js:Политика_безопасности:Пользователь(ispolnitel), js:datetime(task.срок_исполнения), "Задача назначена автоматически"));
                history.дата_действия = udm:(datesec(js:datetime(history.дата_действия), 1));
                
                //<<отправка уведомлений
                var param = {
                    code_subject : 'назначена_задача',
                    code_text : 'назначена_задача',
                    address: [ispolnitel.email],
                    user_login : ispolnitel.логин
                }
                udm:(Задача_заявки:email_task_app(js:Задача:Задача(task), js:variant(param)));
            }
        }
        udm:(задача.заявка.срок_рассмотрения := ДАТАДЕНЬ(TODAY(), 30));
    }
}