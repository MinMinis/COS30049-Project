import React, { useState } from "react";
import Signupbutton from "../components/Button/Signupbutton";
import { Profilefields } from "../data";
import checkEmail from "./../utils/checkEmail";
import checkPassword from "./../utils/checkPassword";
import { ToastContainer, toast } from "react-toastify";
import { useAuth } from "../contexts/AuthContext";
import submission from "./../utils/submission";
import LoadingContainer from "./../components/LoadingContainer";
import handleResponse from "../utils/handleResponse.js";

function Profile() {
  // State to manage form data
  const { user } = useAuth();
  const [loading, setLoading] = useState(false);

  const [form, setForm] = useState({
    email: user.email,
    phone: user.phone,
    password: "",
    confirmPassword: "",
    token: user.token,
  });

  // Function to handle changes in input fields
  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prevForm) => ({ ...prevForm, [name]: value }));
  };

  // Function to handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    for (const key in form) {
      if (form[key] === "") {
        key === "email" && toast.error("Please enter a valid email");
        key === "phone" && toast.error("Please enter a valid phone number");
        key === "password" && toast.error("Please enter a valid password");
        key === "confirmPassword" && toast.error("Passwords do not match");
        setLoading(false);
        return;
      }
    }
    const emailError = checkEmail(form.email);
    if (emailError) {
      toast.error(emailError, { toastId: "toast" });
    }
    const [passwordError, retypePasswordError] = checkPassword(
      form.password,
      form.confirmPassword
    );
    if (passwordError || retypePasswordError) {
      toast.error(passwordError || retypePasswordError, { toastId: "toast" });
    }
    try {
      if (passwordError || retypePasswordError || emailError) {
        throw new Error("Please fix the errors in the form.");
      }
      const response = await submission("updateProfile", "put", form);
      if (response.status === "200 OK" && response.message) {
        toast.success(response.message, { toastId: "toast" });
      } else if (response.status === "401 Unauthorized" && response.message) {
        toast.error(response.message, { toastId: "toast" });
      }
    } catch (error) {
      toast.error(handleResponse(error.message), { toastId: "toast" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="flex flex-col items-center justify-center w-auto overflow-hidden"
      >
        {/* Profile Header */}
        <h1 className="text-3xl text-red-600">Profile settings</h1>
        {/* Profile Fields Section */}
        <div className="flex flex-col p-5">
          {/* Email and Phone Fields */}
          <div className="flex md:flex-row flex-col">
            {Profilefields[0].map((field) => (
              <div
                key={field.name}
                className={`flex ${
                  field.name !== "email" ? "md:ml-10 mt-4 md:mt-0" : ""
                }`}
              >
                <div className="flex flex-col text-2xl">
                  {field.label}:
                  <input
                    className="rounded-lg border-8 w-96 border-white text-black"
                    type={field.type}
                    name={field.name}
                    value={form[field.name]}
                    onChange={handleChange}
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Password Fields */}
          <div className="flex md:flex-row flex-col mt-4">
            {Profilefields[1].map((field) => (
              <div
                key={field.name}
                className={`flex ${
                  field.name !== "password" ? "md:ml-10 mt-4 md:mt-0" : ""
                }`}
              >
                <div className="flex flex-col text-2xl">
                  {field.label}:
                  <input
                    className="rounded-lg border-8 w-96 border-white text-black"
                    type={field.type}
                    name={field.name}
                    value={form[field.name]}
                    onChange={handleChange}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
        {/* Save Changes Button */}
        <div className="flex justify-center items-center pt-10">
          {loading ? (
            <LoadingContainer />
          ) : (
            <Signupbutton type="submit">Save Changes</Signupbutton>
          )}
        </div>
      </form>
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

export default Profile;
