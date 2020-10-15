FUNC_NAME='send_email'
PROJ_ID='wave34-webhelp-vrodriguez'
REGION='europe-west1'

gcloud functions deploy "${FUNC_NAME}" --project="${PROJ_ID}" --region="${REGION}" --trigger-http --allow-unauthenticated --runtime=python37 --source=pyapp --entry-point=main_function
gcloud scheduler jobs create http send-email --schedule='55 8 * * 1-5' --time-zone='Europe/Madrid' --uri="https://${REGION}-${PROJ_ID}.cloudfunctions.net/${FUNC_NAME}"
