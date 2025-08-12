import api from "./index";
import { ExperienceRead, ExperienceCreate, ExperienceUpdate } from "../types";

export async function listExperiences(): Promise<ExperienceRead[]> {
    const { data } = await api.get<ExperienceRead[]>("/admin/experience");
    return data;
}

export async function getExperience(id: number): Promise<ExperienceRead> {
    const { data } = await api.get<ExperienceRead>(`/admin/experience/${id}`);
    return data;
}

export async function createExperience(payload: ExperienceCreate): Promise<ExperienceRead> {
    const { data } = await api.post<ExperienceRead>("/admin/experience", payload);
    return data;
}

export async function updateExperience(
    id: number, 
    payload: ExperienceUpdate
): Promise<ExperienceRead> {
    const { data } = await api.put<ExperienceRead>(`/admin/experience/${id}`, payload)
    return data
}

export async function deleteExperience(id: number): Promise<void> {
    await api.delete(`/admin/experience/${id}`)
}