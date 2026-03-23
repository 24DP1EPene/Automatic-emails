#include <stdio.h>
#include <string.h>

int main(int argc, char const *argv[])
{
    printf("Try out example!\n");
    
    printf("Enter your username: ");
    char username[100];
    scanf("%s", username);
    char emails[5][100]; // Max 5 emails, with up to 100 chars

    for (int i = 0; i < 2; i++)
    {
        printf("Enter your email address: ");
        char email[100];
        scanf("%99s", email); // Reads until the last element: '\0' terminator.
        strcpy(emails[i], email);
    }
    

    FILE *fp = fopen("profiles.txt", "w");

    if (!fp) {
        perror("Failed to open file");
        return 1;
    }

    fprintf(fp, "Username: %s\nEmails:\n\t%s\n\t%s", username, emails[0], emails[1]);

    fclose(fp); // Important on windows!

    return 0;
}