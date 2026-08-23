import {
  GoogleLogin,
  GoogleOAuthProvider,
  googleLogout,
} from "@react-oauth/google";
import { useState } from "react";
import "./google-login.css";

const DEFAULT_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID ?? "";
const DEFAULT_BACKEND_URL = import.meta.env.VITE_BACKEND_URL ?? "";

function decodeGoogleCredential(credential) {
  const encodedPayload = credential.split(".")[1];

  if (!encodedPayload) {
    throw new Error("Credencial inválida.");
  }

  const base64 = encodedPayload
    .replace(/-/g, "+")
    .replace(/_/g, "/");

  const padded = base64.padEnd(
    Math.ceil(base64.length / 4) * 4,
    "=",
  );

  const bytes = Uint8Array.from(
    atob(padded),
    (character) => character.charCodeAt(0),
  );

  const profile = JSON.parse(
    new TextDecoder().decode(bytes),
  );

  if (!profile.sub || !profile.name || !profile.email) {
    throw new Error(
      "O Google não retornou as informações esperadas.",
    );
  }

  if (profile.exp && profile.exp * 1000 < Date.now()) {
    throw new Error("A credencial recebida expirou.");
  }

  return profile;
}

async function sendCredentialToBackend(
  backendUrl,
  credential,
) {
  // Enquanto VITE_BACKEND_URL estiver vazio,
  // nenhuma requisição será feita ao backend.
  if (!backendUrl) return;

  const response = await fetch(
    `${backendUrl.replace(/\/$/, "")}/auth/google`,
    {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ credential }),
    },
  );

  if (!response.ok) {
    throw new Error(
      "O backend não conseguiu validar o login.",
    );
  }
}

function AccountDetails({ profile, onLogout }) {
  return (
    <section
      className="google-account"
      aria-labelledby="google-account-name"
    >
      {profile.picture ? (
        <img
          className="google-avatar"
          src={profile.picture}
          alt={`Foto de ${profile.name}`}
          referrerPolicy="no-referrer"
        />
      ) : (
        <div
          className="google-avatar google-avatar-fallback"
          aria-hidden="true"
        >
          {profile.name.charAt(0).toUpperCase()}
        </div>
      )}

      <div className="google-success-badge">
        <span aria-hidden="true">✓</span>
        Login realizado
      </div>

      <h1 id="google-account-name">
        {profile.name}
      </h1>

      <p className="google-account-email">
        {profile.email}
      </p>

      {profile.email_verified && (
        <p className="google-verified">
          E-mail verificado pelo Google
        </p>
      )}

      <button
        className="google-secondary-button"
        type="button"
        onClick={onLogout}
      >
        Sair da conta
      </button>

      <p className="google-privacy-note">
        Nesta etapa, os dados são exibidos somente
        no navegador. A validação de segurança será
        feita pelo backend.
      </p>
    </section>
  );
}

function LoginContent({ backendUrl }) {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSuccess(response) {
    if (!response.credential) {
      setError(
        "Não foi possível receber a credencial do Google.",
      );
      return;
    }

    setError("");
    setIsLoading(true);

    try {
      const decodedProfile = decodeGoogleCredential(
        response.credential,
      );

      await sendCredentialToBackend(
        backendUrl,
        response.credential,
      );

      setProfile(decodedProfile);
    } catch (caughtError) {
      setError(
        caughtError instanceof Error
          ? caughtError.message
          : "Não foi possível concluir o login.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  function handleLogout() {
    googleLogout();
    setProfile(null);
    setError("");
  }

  if (profile) {
    return (
      <AccountDetails
        profile={profile}
        onLogout={handleLogout}
      />
    );
  }

  return (
    <section
      className="google-login"
      aria-labelledby="google-login-title"
    >
      <h1 id="google-login-title">
        Entrar com Google
      </h1>

      <p className="google-intro">
        Use sua conta Google para continuar.
      </p>

      <div
        className={
          isLoading
            ? "google-official-button google-is-loading"
            : "google-official-button"
        }
      >
        {isLoading ? (
          <span
            className="google-loading-label"
            role="status"
          >
            Conectando…
          </span>
        ) : (
          <GoogleLogin
            onSuccess={handleSuccess}
            onError={() =>
              setError(
                "O login foi cancelado ou não pôde ser concluído.",
              )
            }
            theme="outline"
            size="large"
            shape="rectangular"
            text="continue_with"
          />
        )}
      </div>

      {error && (
        <p
          className="google-error-message"
          role="alert"
        >
          {error}
        </p>
      )}
    </section>
  );
}

function MissingClientId() {
  return (
    <section
      className="google-login"
      aria-labelledby="google-setup-title"
    >
      <h1 id="google-setup-title">
        Entrar com Google
      </h1>

      <p className="google-intro">
        A interface está pronta para receber seu
        Client ID.
      </p>

      <button
        className="google-placeholder"
        type="button"
        disabled
      >
        <span aria-hidden="true">G</span>
        Continuar com Google
      </button>

      <div
        className="google-setup-note"
        role="status"
      >
        Adicione{" "}
        <code>VITE_GOOGLE_CLIENT_ID</code> ao
        arquivo <code>.env</code>.
      </div>
    </section>
  );
}

export default function GoogleLoginPage({
  clientId = DEFAULT_CLIENT_ID,
  backendUrl = DEFAULT_BACKEND_URL,
}) {
  return (
    <main className="google-login-page">
      <div className="google-login-card">
        {clientId ? (
          <GoogleOAuthProvider clientId={clientId}>
            <LoginContent backendUrl={backendUrl} />
          </GoogleOAuthProvider>
        ) : (
          <MissingClientId />
        )}
      </div>
    </main>
  );
}