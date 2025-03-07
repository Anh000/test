void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc){
    adc_value = MAP(buffer, 0, 4095, 0, 100);
}
int main(void)
{
	HAL_Init();
	SystemClock_Config();
	MX_GPIO_Init();
	MX_DMA_Init();
	MX_ADC1_Init();
	/*USER CODE BEGIN 2*/
	HAL_ADC_Start_DMA(&hadc1, &buffer,1);
	while (1)
	{
		/*USER CODE END WHILE*/
        Hum_Level = HAL_GPIO_ReadPin(GPIOA, GPIO_PIN_1);

        if (Hum_Level == 0){
            HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12|GPIO_PIN_13|GPIO_PIN_14|GPIO_PIN_15, GPIO_PIN_SET);
        } else {
            HAL_GPIO_WritePin(GPIOD, GPIO_PIN_12|GPIO_PIN_13|GPIO_PIN_14|GPIO_PIN_15, GPIO_PIN_RESET);
        }
        HAL_Delay(500);
        /*USER CODE BEGIN 3*/
    }
    /*USER CODE END 3*/
}