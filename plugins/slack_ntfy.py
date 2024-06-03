from airflow.hooks.base import BaseHook
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator


def on_failure_callback(context, slack_conn_id):
    # slack_connection_id, rec_sys_slack_connection_id, resource_trace_slack_connection_id, data_report_slack_connection_id
    slack_msg = f"""
        :x: Task Failed.
        *Task*: {context.get('task_instance').task_id}
        *Dag*: {context.get('task_instance').dag_id}
        *Execution Time*: {context.get('data_interval_end')}
        
        <{context.get('task_instance').log_url}|*Logs*>
    """
    slack_webhook_token = BaseHook.get_connection(slack_conn_id).password
    slack_notification = SlackWebhookOperator(
        task_id="slack_notification",
        http_conn_id=slack_conn_id,
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username="airflow",
    )
    return slack_notification.execute(context=context)
