import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import {
    createExperience,
    getExperience,
    updateExperience,
} from "../api/experience";
import { ExperienceCreate } from "../types";
import { useNavigate, useParams } from "react-router-dom";

type FormInputs = ExperienceCreate;

export function ExperienceForm() {
    const { id } = useParams<{ id?: string}>();
    const isEdit = Boolean(id);
    const navigate = useNavigate();
    const { register, handleSubmit, reset } = useForm<FormInputs>();

    useEffect(() => {
        if (isEdit && id) {
            getExperience(Number(id)).then((exp) => {
                reset({
                    company: exp.company,
                    role: exp.role,
                    start: exp.start,
                    description: exp.description,
                    ...(exp.end !== undefined && { end_year: exp.end }),
                });
            });
        }
    }, [id, isEdit, reset]);

    const onSubmit = async (data: FormInputs) => {
        try {
            if (isEdit && id) {
                await updateExperience(Number(id), data);
            } else {
                await createExperience(data);
            }
            navigate("/admin/experience");
        } catch (err: any) {
            alert("Error: " + err.message);
        }
    };

    return (
        <div className="p-4">
            <h1 className="text-xl mb-4">
                {isEdit ? "Edit" : "New"} Experience
            </h1>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 max-w-md">
                <div>
                    <label>Company</label>
                    <input {...register("company", {required: true})} className="w-full border px-2 py-1" />
                </div>
                <div>
                    <label>Role</label>
                    <input {...register("role", {required: true})} className="w-full border px-2 py-1"/>
                </div>
                <div>
                    <label>Start Date</label>
                    <input type="date" {...register("start", {required: true})} className="w-full border px-2 py-1"/>
                </div>
                <div>
                    <label>End Date</label>
                    <input type="date" {...register("end")} className="w-full border px-2 py-1"/>
                </div>
                <div>
                    <label>Description</label>
                    <textarea {...register("description", {required: true})} className="w-full border px-2 py-1" rows={4}/>
                </div>
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">
                    {isEdit ? "Update" : "Create"}
                </button>
                <button type="button" onClick={() => navigate("/admin/experience")} className="ml-2 px-4 py-2 bg-gray-400 text-white rounded">
                    Cancel
                </button>
            </form>
        </div>
    );
}