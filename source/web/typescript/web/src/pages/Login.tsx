import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Form, Input, Button, Typography, Tabs, message } from 'antd'
import { UserOutlined, MailOutlined, LockOutlined } from '@ant-design/icons'
import { authApi } from '../api/auth/authApi'
import Cookies from 'js-cookie'
import { AuthResponse, User } from '../api/types'
import { AxiosError, AxiosResponse } from 'axios'

const { Title } = Typography
const { TabPane } = Tabs

type LoginFormValues = {
	email: string
	password: string
}

type RegisterFormValues = {
	name: string
	email: string
	password: string
	confirmPassword: string
}

const MAX_RETRY_ATTEMPTS = 10
const RETRY_DELAY = 100

const Login = () => {
	const [activeTab, setActiveTab] = useState<'login' | 'register'>('login')
	const [loginLoading, setLoginLoading] = useState(false)
	const [registerLoading, setRegisterLoading] = useState(false)
	const navigate = useNavigate()

	const handleAuthSuccess = (response: AxiosResponse<AuthResponse>) => {
		const { access_token, refresh_token } = response.data
		Cookies.set('access_token', access_token, { expires: 1 })
		Cookies.set('refresh_token', refresh_token, { expires: 7 })

		navigate('/')
	}

	const handleRetryLogin = async (user: User): Promise<boolean> => {
		let attempts = 0
		while (attempts < MAX_RETRY_ATTEMPTS) {
			try {
				const response = await authApi.login(user)

				handleAuthSuccess(response)
				return true
			} catch (error) {
				console.log(error)

				attempts++
				if (attempts < MAX_RETRY_ATTEMPTS) {
					await new Promise(resolve => setTimeout(resolve, RETRY_DELAY))
				}
			}
		}
		return false
	}

	const handleLoginFinish = async (values: LoginFormValues) => {
		try {
			setLoginLoading(true)
			const user: User = {
				user_id: 0,
				email: values.email,
				password_hash: values.password,
				password_salt: '',
				name: '',
				tag: 0,
				avatar_url: '',
			}

			try {
				const response = await authApi.login(user)
				handleAuthSuccess(response)
			} catch (error) {
				if (error instanceof AxiosError && error.response?.status === 404) {
					try {
						const refreshResponse = await authApi.refresh({
							access_token: Cookies.get('access_token') || '',
							refresh_token: Cookies.get('refresh_token') || '',
						})
						handleAuthSuccess(refreshResponse)
					} catch (refreshError) {
						console.log(refreshError)
						Cookies.remove('access_token')
						Cookies.remove('refresh_token')
						message.error('Сессия истекла, войдите заново')
					}
				} else {
					message.error('Ошибка авторизации')
				}
			}
		} finally {
			setLoginLoading(false)
		}
	}

	const handleRegisterFinish = async (values: RegisterFormValues) => {
		try {
			setRegisterLoading(true)
			const user: User = {
				user_id: 0,
				name: values.name,
				email: values.email,
				password_hash: values.password,
				password_salt: '',
				tag: 0,
				avatar_url: '',
			}

			await authApi.register(user)
			const loginSuccess = await handleRetryLogin(user)

			if (!loginSuccess) {
				message.error('Не удалось войти после регистрации')
			}
		} catch (error) {
			console.log(error)
		} finally {
			setRegisterLoading(false)
		}
	}

	return (
		<div style={{ maxWidth: 500, margin: '130px auto', padding: 20 }}>
			<Title level={2} style={{ textAlign: 'center', marginBottom: 20 }}>
				КОВОРКИНГ
			</Title>

			<Tabs
				activeKey={activeTab}
				onChange={key => setActiveTab(key as 'login' | 'register')}
				centered
			>
				<TabPane tab="Вход" key="login">
					<Form<LoginFormValues>
						name="login"
						onFinish={handleLoginFinish}
						layout="vertical"
						requiredMark={false}
					>
						<Form.Item
							name="email"
							rules={[
								{ required: true, message: 'Введите email' },
								{ type: 'email', message: 'Некорректный email' },
							]}
						>
							<Input
								prefix={<MailOutlined />}
								placeholder="Email"
								size="large"
								style={{ fontSize: 16, height: 45 }}
							/>
						</Form.Item>

						<Form.Item
							name="password"
							rules={[{ required: true, message: 'Введите пароль' }]}
						>
							<Input.Password
								prefix={<LockOutlined />}
								placeholder="Пароль"
								size="large"
								style={{ fontSize: 16, height: 45 }}
							/>
						</Form.Item>

						<Form.Item>
							<Button
								type="primary"
								htmlType="submit"
								block
								size="large"
								style={{ height: 45, fontSize: 16 }}
								loading={loginLoading}
							>
								Войти
							</Button>
						</Form.Item>
					</Form>
				</TabPane>

				<TabPane tab="Регистрация" key="register">
					<Form<RegisterFormValues>
						name="register"
						onFinish={handleRegisterFinish}
						layout="vertical"
						requiredMark={false}
					>
						<Form.Item
							name="name"
							rules={[{ required: true, message: 'Введите имя' }]}
						>
							<Input
								prefix={<UserOutlined />}
								placeholder="Имя"
								size="large"
								style={{ fontSize: 16, height: 45 }}
							/>
						</Form.Item>

						<Form.Item
							name="email"
							rules={[
								{ required: true, message: 'Введите email' },
								{ type: 'email', message: 'Некорректный email' },
							]}
						>
							<Input
								prefix={<MailOutlined />}
								placeholder="Email"
								size="large"
								style={{ fontSize: 16, height: 45 }}
							/>
						</Form.Item>

						<Form.Item
							name="password"
							rules={[{ required: true, message: 'Введите пароль' }]}
						>
							<Input.Password
								prefix={<LockOutlined />}
								placeholder="Пароль"
								size="large"
								style={{ fontSize: 16, height: 45 }}
							/>
						</Form.Item>

						<Form.Item
							name="confirmPassword"
							dependencies={['password']}
							rules={[
								{ required: true, message: 'Подтвердите пароль' },
								({ getFieldValue }) => ({
									validator(_, value) {
										if (!value || getFieldValue('password') === value) {
											return Promise.resolve()
										}
										return Promise.reject('Пароли не совпадают')
									},
								}),
							]}
						>
							<Input.Password
								prefix={<LockOutlined />}
								placeholder="Повторите пароль"
								size="large"
								style={{ fontSize: 16, height: 45 }}
							/>
						</Form.Item>

						<Form.Item>
							<Button
								type="primary"
								htmlType="submit"
								block
								size="large"
								style={{ height: 45, fontSize: 16 }}
								loading={registerLoading}
							>
								Зарегистрироваться
							</Button>
						</Form.Item>
					</Form>
				</TabPane>
			</Tabs>
		</div>
	)
}

export default Login
