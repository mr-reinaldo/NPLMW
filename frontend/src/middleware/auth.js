import { useAuthStore } from "@/store/auth"; // Importa o store de autenticação

// Middleware de autenticação
export default async function authMiddleware(to, from, next) {

    // Se a rota requer autenticação
    if(to.matched.some(route => route.meta.auth)){
        // Obtém o store de autenticação
        const authStore = useAuthStore();

        const token = authStore.token; // Obtém o token de acesso
        const type = authStore.type;    // Obtém o tipo de token

        // Define a rota de login
        const loginRoute = {
            name: 'login',
            query: { redirect: to.fullPath }
        }

        // Se o token e o tipo de token existem
        if (token && type) {
            try{

                // Faz uma requisição de teste para verificar se o token é válido
                await authStore.currentUser();

                authStore.isAuthenticated = true; // Define que o usuário está autenticado

                return next(); // Continua para a próxima rota
            } catch (error) {
                return next(loginRoute); // Redireciona para a rota de login
            }
        }

        authStore.isAuthenticated = false; // Define que o usuário não está autenticado
        return next(loginRoute); // Redireciona para a rota de login
    }
    return next(); // Continua para a próxima rota
}