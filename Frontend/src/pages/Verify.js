import React, { useEffect, useRef, useState } from "react";
import VerifyButton from "../components/Button/Verifybutton";
import submission from "./../utils/submission";
import { toast, ToastContainer } from "react-toastify";
import { useNavigate } from "react-router-dom";
import handleResponse from "../utils/handleResponse";
import LoadingContainer from "./../components/LoadingContainer";

function Verify() {
  const inputsRef = useRef([]);
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const inputs = inputsRef.current;

    const handleKeyUp = (e, index) => {
      const currentInput = inputs[index];
      const nextInput = inputs[index + 1];
      const prevInput = inputs[index - 1];

      if (currentInput.value.length > 1) {
        currentInput.value = "";
        return;
      }

      if (
        nextInput &&
        nextInput.hasAttribute("disabled") &&
        currentInput.value !== ""
      ) {
        nextInput.removeAttribute("disabled");
        nextInput.focus();
      }

      if (e.key === "Backspace") {
        inputs.forEach((input, i) => {
          if (i >= index && prevInput) {
            input.setAttribute("disabled", true);
            input.value = "";
            prevInput.focus();
          }
        });
      }
    };

    inputs.forEach((input, index) => {
      input.addEventListener("keyup", (e) => handleKeyUp(e, index));
    });

    window.addEventListener("load", () => inputs[0].focus());

    return () => {
      inputs.forEach((input, index) => {
        if (input) {
          input.removeEventListener("keyup", (e) => handleKeyUp(e, index));
        }
      });
    };
  }, []);
  const handleSubmit = async () => {
    setLoading(true);
    // Extract input values from refs
    const inputValues = inputsRef.current.map((input) => input.value);

    // Combine input values into a single string
    const otp = inputValues.join("");

    // Create JSON object with key-value pair "otp"
    const otpData = { otp };

    try {
      const response = await submission("verify", "post", otpData);
      if (response.error) {
        toast.error(response.error, { toastId: "toast" });
      } else if (response.status === "200 OK") {
        toast.success(`${response.message}`, {
          toastId: "toast",
        });
        setTimeout(() => {
          navigate("/login");
        }, 2000);
      } else if (response.status === 400 || response.message) {
        toast.error(response.message, { toastId: "toast" });
      } else {
        toast.error(
          "We're currently facing connectivity issues. Please try again later.",
          { toastId: "toast" }
        );
      }
    } catch (error) {
      toast.error(handleResponse(error.message), { toastId: "toast" });
      console.log(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="flex justify-center items-center">
        <div className="container">
          <header className="h-[65px] w-[65px] flex items-center justify-center bg-white text-white text-2xl rounded-full">
            <img src="./images/icon/checked.png" alt="check verify" />
          </header>
          <h4 className="text-lg font-bold text-gray-700">Enter OTP Code</h4>
          <form className="text-black" action="#">
            <div className="input-field">
              {[...Array(5)].map((_, index) => (
                <input
                  key={index}
                  ref={(el) => (inputsRef.current[index] = el)}
                  type="number"
                  disabled={index !== 0}
                />
              ))}
            </div>
          </form>
          <div className="pt-4 verify-button-container">
            {loading ? (
              <>
                <LoadingContainer />
              </>
            ) : (
              <VerifyButton handleSubmit={handleSubmit} />
            )}
          </div>
        </div>
      </div>{" "}
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover={false}
        theme="dark"
      />
    </>
  );
}

export default Verify;
