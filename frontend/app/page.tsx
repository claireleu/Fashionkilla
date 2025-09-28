import AuthForm from "./components/AuthForm";

export default function Login() {
  return (
    <AuthForm
      buttonText="Log In"
      buttonHref="/main" // Navigate to the main page
      linkText="Sign up"
      linkHref="/signup"
      linkDescription="Don’t have an account?"
    />
  );
}
