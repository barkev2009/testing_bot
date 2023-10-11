SELECT
    event_date, 
    event_name, 
    time_1, 
    platform, 
    version, 
    user_id, 
    item_name, 
    payment_loan, 
    item_type, 
    item_flow, 
    item_category, 
    last_event_add, 
    last_item_name_add,
    last_currency_add,
    last_item_category_add, 
    app_lang
FROM 
(
    SELECT 
        event_date, 
        event_name, 
        time_1, 
        platform, 
        version, 
        user_id, 
        item_name, 
        payment_loan, 
        item_type, 
        item_flow, 
        item_category,  
        app_lang,
        LAST_VALUE(event_add) OVER (PARTITION BY event_date, event_name, time_1, platform, version, user_id, item_name, payment_loan, item_type, item_flow, item_category, app_lang ORDER BY time_2 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_event_add,
        LAST_VALUE(item_name_add) OVER (PARTITION BY event_date, event_name, time_1, platform, version, user_id, item_name, payment_loan, item_type, item_flow, item_category, app_lang ORDER BY time_2 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_item_name_add,
        LAST_VALUE(currency_add) OVER (PARTITION BY event_date, event_name, time_1, platform, version, user_id, item_name, payment_loan, item_type, item_flow, item_category, app_lang ORDER BY time_2 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_currency_add,
        LAST_VALUE(item_category_add) OVER (PARTITION BY event_date, event_name, time_1, platform, version, user_id, item_name, payment_loan, item_type, item_flow, item_category, app_lang ORDER BY time_2 ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_item_category_add

    FROM
    (
        WITH t1 as (
            SELECT 
                event_date, 
                event_name, 
                event_timestamp as time_1, 
                platform, 
                app_info.version as version,
                user_id, 
                (SELECT value.string_value FROM unnest(event_params) WHERE key='item_name') AS item_name,
                (SELECT value.int_value FROM unnest(event_params) WHERE key='payment_loan') AS payment_loan,
                (SELECT value.string_value FROM unnest(event_params) WHERE key='item_type') AS item_type,
                (SELECT value.string_value FROM unnest(event_params) WHERE key='item_flow') AS item_flow,
                (SELECT value.string_value FROM unnest(event_params) WHERE key='item_category') AS item_category,
                (SELECT value.string_value FROM unnest(user_properties) WHERE key='app_lang') AS app_lang

            FROM `zolotayakorona-75e5e.analytics_151624871.events_202308*` 

            WHERE 
                (app_info.id = 'ru.ftc.zk.dp.qpay-mobile-app-pub' OR app_info.id = 'ru.tsk.ftc.bender.qpay')
                AND (_TABLE_SUFFIX BETWEEN '04' AND '17')
                AND (
                    event_name in ('transfers_payment','transfers_payment_continue','onboarding','onboarding_submit')
                    OR
                    (
                        event_name = 'transfers_infocard' 
                        AND (SELECT value.string_value FROM unnest(event_params) WHERE key='type') ='transferOnLoan'
                        AND (SELECT value.string_value FROM unnest(event_params) WHERE key='item_name')='transferOnLoanUnavailable'
                    )
                )
        ),

        t2 as (
            SELECT 
                event_date, 
                event_name as event_add, 
                event_timestamp as time_2, 
                user_id,
                (SELECT value.string_value FROM unnest(event_params) WHERE key='item_name') AS item_name_add,
                (SELECT value.string_value FROM unnest(event_params) WHERE key='currency') AS currency_add,
                (SELECT value.string_value FROM unnest(event_params) WHERE key='item_category') AS item_category_add

            FROM `zolotayakorona-75e5e.analytics_151624871.events_202308*` 

            WHERE 
                (app_info.id = 'ru.ftc.zk.dp.qpay-mobile-app-pub' OR app_info.id = 'ru.tsk.ftc.bender.qpay')
                AND (_TABLE_SUFFIX BETWEEN '04' AND '17')
                AND event_name IN ('add_to_cart')
        )


        SELECT 
            t1.event_date, 
            t1.event_name, 
            time_1, 
            platform, 
            version, 
            t1.user_id, 
            item_name, 
            payment_loan,
            item_type,
            item_flow,
            item_category,  
            event_add, 
            time_2, 
            item_name_add, 
            currency_add, 
            item_category_add, 
            app_lang
        FROM t1 
        LEFT JOIN t2 ON (
            t1.user_id = t2.user_id 
            AND t1.event_date = t2.event_date 
            AND time_1 > time_2
        )
    )
)


GROUP BY 
    event_date, 
    event_name, 
    time_1, 
    platform, 
    version, 
    user_id, 
    item_name, 
    payment_loan, 
    item_type, 
    item_flow, 
    item_category, 
    last_event_add, 
    last_item_name_add,
    last_currency_add,
    last_item_category_add, 
    app_lang