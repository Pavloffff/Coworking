import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Login from './pages/Login'
import Main from './pages/Main'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useEffect } from 'react'
import Cookies from 'js-cookie'

const queryClient = new QueryClient()
function App() {
	useEffect(() => {
		const access_token = localStorage.getItem('access_token')
		const refresh_token = localStorage.getItem('refresh_token')
		if (
			access_token &&
			refresh_token &&
			!Cookies.get('access_token') &&
			!Cookies.get('refresh_token')
		) {
			Cookies.set('access_token', access_token)
			Cookies.set('refresh_token', refresh_token)
		}
	}, [])
	return (
		<QueryClientProvider client={queryClient}>
			<Router>
				<Routes>
					<Route path="/login" element={<Login />} />
					<Route path="/" element={<Main />} />
				</Routes>
			</Router>
		</QueryClientProvider>
	)
}
export default App
