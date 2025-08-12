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