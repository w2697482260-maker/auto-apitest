pipeline {
    agent any

    parameters {
        choice(name: 'ENV', choices: ['test', 'staging', 'dev'], description: '测试环境')
        choice(name: 'TEST_TYPE', choices: ['all', 'smoke', 'regression', 'bos', 'admin', 'staff'], description: '测试类型')
        choice(name: 'STOCK_TYPE', choices: ['all', 'hk_us', 'unlisted', 'a_stock'], description: '股票类型')
    }

    environment {
        TEST_ENV = "${params.ENV}"
    }

    stages {
        stage('代码检出') {
            steps {
                echo '检出代码...'
                checkout scm
            }
        }

        stage('环境准备') {
            steps {
                echo '安装依赖...'
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
                '''
            }
        }

        stage('执行测试') {
            steps {
                script {
                    echo "测试环境: ${params.ENV}"
                    echo "测试类型: ${params.TEST_TYPE}"
                    echo "股票类型: ${params.STOCK_TYPE}"

                    def markers = ""
                    if (params.TEST_TYPE != 'all') {
                        markers = "-m ${params.TEST_TYPE}"
                    }

                    if (params.STOCK_TYPE != 'all') {
                        if (markers == "") {
                            markers = "-m ${params.STOCK_TYPE}"
                        } else {
                            markers = "-m \\\"${params.TEST_TYPE} and ${params.STOCK_TYPE}\\\""
                        }
                    }

                    // 使用 catchError 确保即使测试失败也继续生成报告
                    catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                        sh """
                            . .venv/bin/activate
                            export TEST_ENV=${params.ENV}
                            pytest ${markers} --reruns 1 --reruns-delay 2
                        """
                    }
                }
            }
        }

        stage('生成报告') {
            steps {
                echo '生成Allure报告...'
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'reports/allure-results']]
                    ])
                }
            }
        }

        stage('飞书通知') {
            steps {
                script {
                    echo '飞书通知已通过 pytest 插件自动发送'
                    echo "报告地址: ${BUILD_URL}allure"
                }
            }
        }
    }

    post {
        always {
            echo '清理工作完成'
        }
        success {
            echo '✅ 测试执行成功'
        }
        failure {
            echo '❌ 测试执行失败'
        }
    }
}
