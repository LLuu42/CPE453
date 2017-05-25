#include <stdio.h>
#include <stdlib.h>
//#include "schedSim.h"

char *readline (FILE *fp, char **buffer) 
{
   int ch;
   size_t buflen = 0, 
   nchar = 10;

   *buffer = malloc (nchar); 
   if (*buffer == NULL) 
   {
      fprintf (stderr, "Not enough memory space. ): \n");
      return NULL;
   }

   while ((ch = fgetc(fp)) != '\n' && ch != EOF) 
   {
       (*buffer)[buflen++] = ch;

        if (buflen + 1 >= nchar) 
        { 
           char *tmp = realloc (*buffer, nchar * 2);
           if (!tmp) 
           {
               fprintf (stderr, "reallocate failed ): \n");
               (*buffer)[buflen] = 0;
               return *buffer;
           }
           *buffer = tmp;
           nchar *= 2;
       }
   }

   (*buffer)[buflen] = '\0';
   if (ch == EOF) 
   {
      free (*buffer);
      *buffer = NULL;
   }

   return *buffer;
}
