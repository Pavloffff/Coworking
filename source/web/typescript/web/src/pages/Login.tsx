import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Form, Input, Button, Typography, Tabs } from 'antd'
import { UserOutlined, MailOutlined, LockOutlined } from '@ant-design/icons'
import { authApi } from '../api/auth/authApi'

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

const Login = () => {
	const [activeTab, setActiveTab] = useState<'login' | 'register'>('login')
	const [loading, setLoading] = useState(false)
	const navigate = useNavigate()

	const handleLoginFinish = async (values: LoginFormValues) => {
		try {
			setLoading(true)
			const user = {
				email: values.email,
				password_hash: values.password,
				password_salt: '',
				user_id: 0,
				name: '',
				tag: 0,
				avatar_url: '',
			}
			const success = await authApi.login(user)
			if (success) {
				navigate('/')
			}
		} catch (error) {
			console.log(error)
		} finally {
			setLoading(false)
		}
	}

	const handleRegisterFinish = async (values: RegisterFormValues) => {
		try {
			setLoading(true)
			const user = {
				email: values.email,
				password_hash: values.password,
				password_salt: '',
				user_id: 0,
				name: values.name,
				tag: 0,
				avatar_url: '',
			}
			await authApi.register(user)
			let success = false
			let attempts = 0
			const maxAttempts = 10
			const delay = 100 // 0.1 секунды

			while (!success && attempts < maxAttempts) {
				attempts++
				success = await authApi.login(user)

				if (!success) {
					if (attempts < maxAttempts) {
						await new Promise(resolve => setTimeout(resolve, delay))
					}
				} else {
					navigate('/')
				}
			}
		} catch (error) {
			console.log(error)
		} finally {
			setLoading(false)
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
								loading={loading && activeTab === 'login'}
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
								loading={loading && activeTab === 'register'}
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
