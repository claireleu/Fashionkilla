import AuthForm from "../components/AuthForm";

export default function Signup() {
  return (
    <AuthForm
      buttonText="Sign Up"
      buttonHref="/main" // Navigate to the main page
      linkText="Log in"
      linkHref="/"
      linkDescription="Already have an account?"
    />
  );
}