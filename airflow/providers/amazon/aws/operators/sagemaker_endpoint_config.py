#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from airflow.exceptions import AirflowException
from airflow.providers.amazon.aws.operators.sagemaker_base import SageMakerBaseOperator


class SageMakerEndpointConfigOperator(SageMakerBaseOperator):
    """
    Create a SageMaker endpoint config.

    This operator returns The ARN of the endpoint config created in Amazon SageMaker

    :param config: The configuration necessary to create an endpoint config.

        For details of the configuration parameter see :py:meth:`SageMaker.Client.create_endpoint_config`
    :type config: dict
    :param aws_conn_id: The AWS connection ID to use.
    :type aws_conn_id: str
    """

    integer_fields = [['ProductionVariants', 'InitialInstanceCount']]

    def __init__(self, *, config: dict, **kwargs):
        super().__init__(config=config, **kwargs)

        self.config = config

    def execute(self, context) -> dict:
        self.preprocess_config()

        self.log.info('Creating SageMaker Endpoint Config %s.', self.config['EndpointConfigName'])
        response = self.hook.create_endpoint_config(self.config)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise AirflowException(f'Sagemaker endpoint config creation failed: {response}')
        else:
            return {'EndpointConfig': self.hook.describe_endpoint_config(self.config['EndpointConfigName'])}
