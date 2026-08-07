export interface ExperienceRead {
    id: number;
    company: string;
    role: string;
    start: string;
    end?: string;
    description: string;
}

export interface ExperienceCreate {
    company: string;
    role: string;
    start: string;
    end?: string;
    description: string;
}

export interface ExperienceUpdate {
    company?: string;
    role?: string;
    start?: string;
    end?: string;
    description?: string;
}

export interface ExperienceEntry {
    role: string;
    company: string;
    start: string;
    end?: string;
    description: string;
}

export interface EducationEntry {
    institution: string;
    degree: string;
    start: string;
    end?: string;
    details?: string;
}

export interface SkillEntry {
    name: string;
    proficiency?: string;
    category?: string;
    years_experience?: number;
    last_used?: string;
    tools?: string[];
    description?: string;
}

export interface CVData {
    name: string;
    title: string;
    experience: ExperienceEntry[];
    education: EducationEntry[];
    skills: SkillEntry[];
}